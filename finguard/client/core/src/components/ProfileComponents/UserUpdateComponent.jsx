"use client"

import EmailUpdateComponent from "./Segments/EmailUpdateComponent"
import PasswordUpdateComponent from "./Segments/PasswordUpdateComponent"
import UsernameUpdateComponent from "./Segments/UsernameUpdateComponent"

function UserUpdateComponent() {
    
    return (
        <div className="flex flex-col items-center ">
           
           <UsernameUpdateComponent/>
            <EmailUpdateComponent />
            <PasswordUpdateComponent/>
        </div>
    )
}


export default UserUpdateComponent