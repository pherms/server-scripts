import * as dotenv from 'dotenv';
import express from 'express';
import http from 'http';
import bodyParser, { urlencoded } from 'body-parser';
import cookieParser from 'cookie-parser';
import compression from 'compression';
import cors from 'cors';

import userRouter from './router/user.router';
import authRouter from './router/auth.router';
import configurationRouter from './router/configuration.router';

dotenv.config();

if (!process.env.PORT) {
    process.exit(1);
}

const PORT: number = parseInt(process.env.PORT as string, 10);

const app = express();
const corsOptions = {
    origin: true,
    credentials: true
}
// app.use(cors({
//     credentials: true,
//     origin: true,
// }));
app.use(cors(corsOptions));
app.use(compression());
app.use(cookieParser());
app.use(urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.use('/api/v1/auth',authRouter);
app.use('/api/v1/users',userRouter);
app.use('/api/v1/configuration',configurationRouter);

const server = http.createServer(app);

server.listen(PORT,() => {
    console.log(`Listening on port: ${PORT}`);
});

