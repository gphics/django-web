"use client"
import sendRequest from "@/utils/requestSender"
import { useContext, useState } from "react"
import { toast } from "react-toastify"
import { ProfileContext } from "../profileReducer"


export default function UsernameUpdateComponent() {
    const {state, dispatch} = useContext(ProfileContext)
    const [username, setUsername] = useState(state?.user?.username)

    async function updateInfo(e) {
        e.preventDefault()
        if (!username) {
            toast.warning("username must be provided")
            return
        }

        // updating isLoading
        dispatch({ type: "TOGGLE_LOADING" })
        
        const url = "account/update-username"
        const body = { username}
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
            <legend className="text-center font-medium px-3 capitalize">username Update Form</legend>

            <input onChange={(e) => setUsername(e.target.value)} type="username" name="username" value={username} className="bg-primary-color w-[95%] mx-auto h-[45px] outline-none font-medium border-none text-white rounded-sm my-1 px-2 focus:bg-accent-color focus:text-primary-color transition-all duration-200" required />
            <button type="submit" className="my-2 mx-auto font-medium bg-accent-color w-fit px-5 py-2 cursor-pointer text-white  rounded-md hover:bg-primary-color transition-all duration-200">Submit</button>
        </fieldset>

    </form>
}