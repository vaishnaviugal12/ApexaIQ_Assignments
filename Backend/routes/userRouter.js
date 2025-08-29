import express from "express";
import { loginUser,registerUser,deleteUser,getUser } from "../controller/usercontroller.js";


const userRouter = express.Router()

userRouter.post("/register", registerUser)
userRouter.post("/login",loginUser)
userRouter.delete("/:id", deleteUser)
userRouter.get("/:id", getUser); 
export default userRouter;