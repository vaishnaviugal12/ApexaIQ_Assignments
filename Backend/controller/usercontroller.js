import userModel from "../model/usermodel.js";
import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
import validator from "validator"


//Creating token important
const createToken =  (id,role) =>{
 return jwt.sign({id,role},process.env.JWT_SECRET )
}





//login user
const loginUser = async (req,res)=>{
const {email,password} =req.body;
try{
     const user = await userModel.findOne({email});

     if(!user){
         return res.json({success:false, message:"user does not exist "});
     }

     const isMatch = await bcrypt.compare(password,user.password);
     if(!isMatch){
          return res.json({success:false, message:"Invalid Credentials"});

     }
//Calling the token
     const token =createToken(user._id,user.role);
     res.json({success:true,token, role:user.role});

} catch(error){
   console.log("error");
   res.json({success:false, message:"Error"});
}
}



// Delete user
const deleteUser = async (req, res) => {
    try {
        const { id } = req.params;
        
        // Optional: Check if user exists before deleting
        const user = await userModel.findById(id);
        if (!user) {
            return res.json({ success: false, message: "User not found" });
        }
        
        await userModel.findByIdAndDelete(id);
        res.json({ success: true, message: "User deleted successfully" });
    } catch (error) {
        console.log("Error deleting user:", error);
        res.json({ success: false, message: "Error deleting user" });
    }
}


//register usuer
const registerUser = async (req,res) =>{

     const {name,password,email} =req.body;
try{
 //validating email format and strong password
    if(!validator.isEmail(email)){
         return res.json({success:false, message:"please enter a valid email "})
    }

    if(password.length<8){
         return res.json({success:false, message:"please enter a strong password "})
    }


    const exist = await userModel.findOne({email});
    if(exist){
        return res.json({success:false, message:"user already exist"})
    }
    
   

    //hashing user password using bycrypt
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password,salt);
  
    //registering the new user 
    const newUser = new userModel({
        name:name, 
        email:email,
        password: hashedPassword,
        role:"user"
    })
  
 //storing the data of the user in database
  const  user =   await newUser.save();
  //creating the token using users id
  const token = createToken(user._id,user.role);
  res.json({success:true,token,role:user.role});
}
catch(error){
console.log("error");
res.json({success:false,message:error})
}
}

// ✅ Get user details by ID
const getUser = async (req, res) => {
  try {
    const { id } = req.params;

    const user = await userModel.findById(id).select("-password"); // exclude password
    if (!user) {
      return res.json({ success: false, message: "User not found" });
    }

    res.json({ success: true, user });
  } catch (error) {
    console.log("Error fetching user:", error);
    res.json({ success: false, message: "Error fetching user" });
  }
};

export{loginUser,registerUser,deleteUser,getUser};