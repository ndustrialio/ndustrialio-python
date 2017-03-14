import os
import socket
import paramiko


class SFTPConnectionException(Exception):
    pass


class SFTPClient():
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.transport = None
        self.sftp = None
        self.connect()

    def connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.hostname, self.port))
        except Exception as e:
            raise SFTPConnectionException('Socket connection to SFTP server failed')

        try:
            self.transport = paramiko.Transport(sock)
            try:
                self.transport.start_client()
            except paramiko.SSHException:
                raise SFTPConnectionException('SSH negotiation to SFTP Server failed')

            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
            except IOError:
                try:
                    keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
                except IOError:
                    raise SFTPConnectionException('Unable to open host keys file at ~/ssh/known_hosts')
                    keys = {}

            # check server's host key -- this is important.
            key = self.transport.get_remote_server_key()
            if self.hostname not in keys:
                print('*** WARNING: Unknown host key!')
            elif key.get_name() not in keys[self.hostname]:
                print('*** WARNING: Unknown host key!')
            elif keys[self.hostname][key.get_name()] != key:
                print('*** WARNING: Host key has changed!!!')
                raise SFTPConnectionException('Host key of SFTP server has changed! Connection aborted')
            else:
                pass
        except Exception as e:
            try:
                self.transport.close()
            except:
                pass
            raise

    def rsa_auth(self, username, private_key_path):

        try:
            ## now manually go in and connect using a private key
            if len(private_key_path) == 0:
                print('Must provide private_key_path environment variable!')
                # add custom exception here
                raise SFTPConnectionException('Must provide private key path')

            if self.transport is None:
                raise SFTPConnectionException('No Connection present')

            if self.transport.is_authenticated():
                raise SFTPConnectionException('Connection has already been made')

            key = paramiko.RSAKey.from_private_key_file(private_key_path, '')  # no password for the private key
            self.transport.auth_publickey(username, key)
            if not self.transport.is_authenticated():
                self.transport.close()
                raise SFTPConnectionException('*** Authentication failed. :(')

        except Exception as e:
            try:
                self.transport.close()
            except:
                pass
            raise

    def password_auth(self, username, password):
        try:
            self.transport.auth_password(username, password)
        except Exception as e:
            try:
                self.transport.close()
            except:
                pass
            raise e

    def getClient(self):

        if self.transport is None:
            raise SFTPConnectionException('Connection to server not initiated!')

        if not self.transport.is_authenticated():
            raise SFTPConnectionException('Connection to server not authenticated!')

        try:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)

        except Exception as e:
            try:
                self.transport.close()
            except:
                pass
            raise

        return self.sftp

    def close(self):
        if self.transport is None:
            raise SFTPConnectionException('Connection to server not initiated!')

        self.transport.close()
