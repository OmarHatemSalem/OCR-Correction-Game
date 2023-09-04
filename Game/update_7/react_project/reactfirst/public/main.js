
const { app, BrowserWindow } = require('electron');
//const path = require('path');
//const url = require('url');
const waitOn = require('wait-on');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      
      enableRemoteModule: true,
      nodeIntegration: true, // causes warning 
      contextIsolation: false, // causes warning 
      webSecurity: false // causes warning 
    },
  });

/*
  const indexPath = path.join(__dirname, `../dist/index.html`); // Update the path here
  console.log('__dirname:', __dirname);
  console.log('Index HTML path:', indexPath);

  mainWindow.loadURL(
    url.format({
      pathname: indexPath,
      protocol: 'file:',
      slashes: true,
    })
  );
*/

  // Wait for the React development server to be ready
  waitOn({ resources: ['http://localhost:3000'] }).then(() => {
    // Load the React app URL once the server is ready
    mainWindow.loadURL('http://localhost:3000');
  });


  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  mainWindow.webContents.openDevTools();
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

