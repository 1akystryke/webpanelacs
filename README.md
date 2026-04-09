# AC Server Web Panel

A web-based control panel for remotely managing Assetto Corsa racing simulator servers. The application provides a user-friendly interface for configuring server settings, managing tracks and cars, and adjusting race parameters without requiring direct access to the server files.

## Features

<img width="2537" height="1186" alt="image" src="https://github.com/user-attachments/assets/bccf440d-9d7b-4758-82ba-5abd703518e1" />

## Installation Guide

### Prerequisites

- Docker and Docker Compose ([Installation Guide](https://docs.docker.com/engine/install/))
- An Assetto Corsa server downloaded via SteamCMD

### Installing Assetto Corsa Server via SteamCMD

The following instructions are for **Debian/Ubuntu**. Other systems may require minor adjustments.

1. **Install SteamCMD**

```bash
sudo apt-get install lib32gcc-s1
curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
```

2. **Run SteamCMD**

```bash
./linux32/steamcmd
```

3. **Install Assetto Corsa Dedicated Server**

```bash
force_install_dir <path>
login <username> <password>
app_update 302550 validate
```

- `<path>` – the installation path for the Assetto Corsa server. This path must also be specified in the `.env` file. Make sure the directory exists.
- `<username>` `<password>` – your Steam account credentials. **Important:** The Steam account must own Assetto Corsa.

### Running the Web Panel with Docker

1. **Clone or download the project**

```bash
git clone https://github.com/1akystryke/webpanelacs.git
cd webpanelacs
```

or

```bash
curl https://codeload.github.com/1akystryke/webpanelacs/zip/refs/heads/main -o zip.zip
unzip zip.zip
cd webpanelacs
```

2. **Create a `.env` file** in the project root with your configuration:

```env
SERVER_PATH=/path/to/your/ac/server   # path to your Assetto Corsa server installation
PORT=5002
AUTH_USER=admin
AUTH_PASS=your_secure_password
SESSION_SECRET=your_random_secret_key
```

3. **Build and run the application using Docker Compose**

```bash
docker-compose up -d
```

4. **Access the web panel**

- Open your browser and go to `http://your_ip:5002`
- Log in using the credentials specified in the `.env` file
