"use client"
import { FaUser } from "react-icons/fa";
import { RiLockPasswordFill } from "react-icons/ri";
import { useState } from "react"
import InputComponent from "../InputComponent"
import Link from "next/link"
import { toast } from "react-toastify";
import sendRequest from "@/utils/requestSender";
import CookieManager from "@/utils/cookieManager";
import { useRouter } from "next/navigation";
import FullPageLoadingComponent from "./FullPageLoadingComponent";


function AuthForm({ category }) {
    const router= useRouter()
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [passwordState, setPasswordState] = useState("password")
    const [isLoading, setIsLoading] = useState(false)

    const inputArr = [
        { type: "text", value: username, name: "username", onChangeHandler: usernameChangeHandler, Icon: FaUser },
        { type: passwordState, value: password, name: "password", onChangeHandler: passwordChangeHandler, Icon: RiLockPasswordFill, others: { minLength: 6 } },
    ]

    function passwordChangeHandler(e) {
        setPassword(e.target.value)
    }
    function usernameChangeHandler(e) {
        setUsername(e.target.value)
    }
    function changePasswordInputType() {
        setPasswordState(prev => prev === "text" ? "password" : "text")
    }

    const regText = "Don't have an account yet ? "
    const loginText = "Already have an account ?"

    function validateInput() {
        if (!username || !password) {
            toast.warn("username and password must be provided")
            setIsLoading(!true)
            return
        }
        if (password.length < 6) {
            toast.warn("Password length must be greater than 5")
            setIsLoading(!true)
        } 
    }
    async function submitHandler(e) {
        e.preventDefault()
        const body = { username, password }
        setIsLoading(true)

        // validating input
        validateInput()
        const url = category === "login" ? "account/auth" : "account/reg"
        const res = await sendRequest(url, {body, method:"post", isAuth:false})
        setIsLoading(!true)
        console.log(res)
        // if no error
        if (res.success) {
            const cookieMgt = CookieManager()
            const { msg: { token } } = res.data
            cookieMgt.setCookie(token)
            router.replace("/dashboard")
        } else {
      
            toast.error(res.err[0])
        }


    }
    return (
        <form onSubmit={submitHandler} className="flex flex-col w-[95%] max-w-[400px] bg-primary-color h-[80vh] max-h-[400px] items-center rounded-md">
            {isLoading && <FullPageLoadingComponent/>}
            <section className="flex flex-col my-5 justify-center items-center">
                <h2 className="text-accent-color poppins-bold">Welcome</h2>
                {category === "login" ?
                    <p className="my-1 text-[.9em]"> {regText} <Link href={"/auth/register"} className="poppins-bold text-accent-color italic" >Sign Up</Link> </p>
                    :
                    <p className="my-1 text-[.9em]"> {loginText}  <Link href={"/auth/login"} className="poppins-bold text-accent-color italic">Sign In</Link>  </p>}
            </section>
            {inputArr.map((items, index) => {

                return <InputComponent {...items} key={index} />
            })}

            {/* for changing the visibility of the password input */}
            <section className=" w-[95%] my-2 pl-1 flex items-center">
                <input onChange={changePasswordInputType} className="size-4 outline-none" type="checkbox" />
                <label className="text-[0.9em] ml-2" htmlFor="showPassword">Show Password</label>
            </section>

            {/* form submission */}
            <button type="submit" className="bg-accent-color px-6 mt-1 poppins-bold rounded-md py-2 hover:text-primary-color cursor-pointer" onClick={submitHandler}>Submit</button>
        </form>
    )
}

export default AuthForm

