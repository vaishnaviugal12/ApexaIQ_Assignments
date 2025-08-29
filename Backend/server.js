import express from "express";
import connectDB from "./config.js/db.js";
import userRouter from "./routes/userRouter.js";
//import cors from "cors"; // Import cors package
// Import env file
import 'dotenv/config';

// App config
const app = express();
const port = process.env.PORT || 4000;

// Middleware
app.use(express.json());


// DB connection
connectDB();


//api endpoint for user
app.use('/api/user',userRouter)

// Test route
app.get("/", (req, res) => {
  res.send("Auth API is working!");
});

app.listen(port, () => console.log(`Server started on port ${port}`));