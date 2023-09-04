const express = require('express');
const cors = require('cors');
const fs = require('fs-extra');
const path = require('path');
const serveStatic = require('serve-static'); // Import the serve-static module

const app = express();
const port = 5000;

app.use(cors({
    credentials: true
}));

const testFolderPath = path.join(__dirname, 'test');

// Use serve-static to serve static files from the 'test' folder
app.use('/images', serveStatic(testFolderPath));

const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif']; 

app.get('/images', (req, res) => {
  fs.readdir(testFolderPath, (err, files) => {
    if (err) {
      console.error('Error reading pictures from folder:', err);
      res.status(500).send('Error reading pictures from folder');
      return;
    }
    const imageFiles = files.filter((fileName) =>
      imageExtensions.some((ext) => fileName.toLowerCase().endsWith(ext))
    );
    const imageUrls = imageFiles.map((fileName) => `http://localhost:5000/images/${fileName}`);
    res.json(imageUrls);
  });
});

app.post('/save/:fileName', express.text(), (req, res) => {
    const { fileName } = req.params;
    const textFilePath = path.join(testFolderPath, `${fileName}.txt`);
    fs.writeFile(textFilePath, req.body, (err) => {
        if (err) {
            console.error('Error saving text file:', err);
            res.status(500).send('Error saving text file');
            return;
        }
        res.send('Text file saved successfully');
    });
});

  
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
