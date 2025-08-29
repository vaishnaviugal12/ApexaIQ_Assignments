import mongoose from "mongoose";

 const connectDB = async ()=>{
  await mongoose.connect(process.env.MONGPDB_URL).then(()=>console.log("db connected"))
}
export default connectDB;
