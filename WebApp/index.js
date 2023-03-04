const express = require('express')
const path = require('path')
const multer = require('multer')
const { spawn } = require('child_process')

const app = express()

app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'ejs')

app.use(express.static(path.join(__dirname, 'public')))

app.get('/asl', (req, res) => {
    res.render('asl', { videoPresent: false })
})

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/uploads/')
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
        cb(null, file.fieldname + '-' + uniqueSuffix + '.' + file.originalname.split('.')[1])
    }
})

const upload = multer({ storage })
app.post('/upload', upload.single('userVideo'), async (req, res) => {
    const file = req.file
    const { filename } = file
    const name = filename.split('.')[0], extension = filename.split('.')[1]

    const python = spawn('python', ['./process_video.py', `${name}.${extension}`, `${name}.vtt`])
    python.stdout.on('data', (data) => {
        console.log(data.toString())
    })

    python.on('exit', () => {
        console.log('Created subtitle')
        res.render('asl', { videoPresent: true, videoName: file.filename, subtitleName: `${name}.vtt` })
    })
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`)
})