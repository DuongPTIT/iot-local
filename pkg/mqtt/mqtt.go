package mqtt

import (
	"crypto/tls"
	"fmt"
	"io"
	"net"

	"github.com/mainflux/mainflux/logger"
	"github.com/mainflux/mainflux/pkg/errors"
	"iot-local/pkg/session"
	mptls "iot-local/pkg/tls"
)

var (
	errCreateListener = errors.New("failed creating TLS listener")
)

// Proxy is main MQTT proxy struct
type Proxy struct {
	address string
	target  string
	handler session.Handler
	logger  logger.Logger
}

// New returns a new mqtt Proxy instance.
func New(address, target string, handler session.Handler, logger logger.Logger) *Proxy {
	return &Proxy{
		address: address,
		target:  target,
		handler: handler,
		logger:  logger,
	}
}

func (p Proxy) accept(l net.Listener) {
	for {
		conn, err := l.Accept()
		if err != nil {
			p.logger.Warn("Accept error " + err.Error())
			continue
		}

		p.logger.Info("Accepted new client")
		go p.handle(conn)
	}
}

func (p Proxy) handle(inbound net.Conn) {
	defer p.close(inbound)
	clientCert, err := mptls.ClientCert(inbound)
	if err != nil {
		p.logger.Error("Failed to get client certificate: " + err.Error())
		return
	}

	s := session.New(inbound, p.handler, p.logger, clientCert)

	if err = s.Stream(); !errors.Contains(err, io.EOF) {
		p.logger.Warn("Broken connection for client: " + s.Client.ID + " with error: " + err.Error())
	}
}

// Listen of the server, this will block.
func (p Proxy) Listen() error {
	l, err := net.Listen("tcp", p.address)
	if err != nil {
		return err
	}
	defer l.Close()

	// Acceptor loop
	p.accept(l)

	p.logger.Info("Server Exiting...")
	return nil
}

// ListenTLS - version of Listen with TLS encryption
func (p Proxy) ListenTLS(tlsCfg *tls.Config) error {

	l, err := tls.Listen("tcp", p.address, tlsCfg)
	if err != nil {
		return errors.Wrap(errCreateListener, err)
	}
	defer l.Close()

	// Acceptor loop
	p.accept(l)

	p.logger.Info("Server Exiting...")
	return nil
}

func (p Proxy) close(conn net.Conn) {
	if err := conn.Close(); err != nil {
		p.logger.Warn(fmt.Sprintf("Error closing connection %s", err.Error()))
	}
}