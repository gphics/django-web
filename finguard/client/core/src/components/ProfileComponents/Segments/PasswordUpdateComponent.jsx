"use client"
import sendRequest from "@/utils/requestSender"
import { useContext, useState } from "react"
import { toast } from "react-toastify"
import { ProfileContext } from "../profileReducer"


export default function PasswordUpdateComponent() {
    const { state, dispatch } = useContext(ProfileContext)
    const [password, setPassword] = useState({ new_password: "", old_password: "" })
    const [showPassword, setShowPassword] = useState(false)


    function passwordValidation() {
        const data = Object.entries(password)
        let status = true

        data.map(elem => {
            const key = elem[0]
            const value = elem[1]

            if (!value) {
                toast.warning(key + " must be provided", {toastId:key})
                status = false
            }
            if (value.length < 6) {
                toast.warning(key + " length must be greater than 5", { toastId: key })
                status = false
            }
        })
        if (password.old_password === password.new_password) {
            toast.warning("Both old and new passwords must be different", { toastId: 1})
            status = false
        }
        return status

    }
    async function updateInfo(e) {
        e.preventDefault()

        // validation
        const is_valid = passwordValidation()
        if (!is_valid) {
            return
        }

        // updating isLoading
        dispatch({ type: "TOGGLE_LOADING" })

        const url = "account/update-password"
        const body = { ...password }
        const method = "PUT"
        const res = await sendRequest(url, { method, body })

        // updating isLoading
        dispatch({ type: "TOGGLE_LOADING" })


        if (res?.err || !res.success) {
            toast.error(res?.err?.[0])
            return
        }

        toast.success(res?.data?.msg)
        state?.refresh()
    }
    return <form onSubmit={updateInfo} className="my-2 w-full max-w-[400px]">

        <fieldset className="border-2 flex flex-col rounded-md">
            <legend className="text-center font-medium px-3 capitalize ">password Update Form</legend>

            {/* Old password */}
            <div className="flex flex-col my-2 items-center">
                <label className="w-[95%] font-medium my-1" htmlFor="old_password">Old Password</label>
                <input onChange={(e) => {
                    const { value, name } = e.target
                    setPassword(prev => ({ ...prev, [name]: value }))
                }} type={showPassword ? "text" : "password"} name="old_password" value={password?.old_password} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" required />
            </div>

            {/* New Passsword */}
            <div className="flex flex-col my-2 items-center">
                <label className="w-[95%] font-medium my-1" htmlFor="new_password">New Password</label>
                <input onChange={(e) => {
                    const { value, name } = e.target
                    setPassword(prev => ({ ...prev, [name]: value }))
                }} type={showPassword ? "text" : "password"} name="new_password" value={password?.new_password} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" required />
            </div>

            {/* Password visibility action */}
            <div className="w-[95%] mx-auto">
                <input onChange={(e) => {

                    setShowPassword(e.target?.checked)
                }} type="checkbox" name="show_password" id="" /> <span>Show Password</span>
            </div>
            <button type="submit" className="my-2 mx-auto font-medium bg-accent-color w-fit px-5 py-2 cursor-pointer text-white  rounded-md hover:bg-primary-color transition-all duration-200">Submit</button>
        </fieldset>

    </form>
}