
import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
    name:{type:String, required:true},
    email:{type:String, required:true},
    password:{type:String, required:true},
    role: { type: String, enum: ['user', 'admin'], default: 'user' },
    cartData:{type:Object,default:{}}
},{minimize:false})
//we added the minimize so thaqt the cart data entry will be created without any data

//the or operator is used beacuse it create the model only if not created
//this help to avoid the issue when start the server again our samemodel dont get created again and again
const userModel = mongoose.model.user || mongoose.model("user", userSchema);
export default userModel;



