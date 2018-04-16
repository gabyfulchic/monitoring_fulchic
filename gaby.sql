CREATE DATABASE IF NOT EXISTS monitoring;
use monitoring;

CREATE TABLE IF NOT EXISTS websites (
	id INT NOT NULL AUTO_INCREMENT,
	url VARCHAR(500),
	status int(11),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS user (
	in INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(500),
	password VARCHAR(500),
	is_admin BOOLEAN,
	PRIMARY KEY (id)
);
#tenez je vous laisse votre utilisateur possédant le mdp password au moins vous êtes pas perdus !
INSERT INTO user (email, password, is_admin) VALUES ('someone@yopmail.com', '$argon2i$v=19$m=512,t=2,p=2$07qXMsb4P4fQ+p9T6l3rvQ$hWU817VMNDP/E9l21rYOKQ', true);
#les sites vous les ajouterez vous mêmes grâce au site MyMonitor.com
