"use client"

import { useState } from "react"
import FullPageLoadingComponent from "../Others/FullPageLoadingComponent"
import { toast, ToastContainer } from "react-toastify"
import sendRequest from "@/utils/requestSender"
import { useRouter } from "next/navigation"

function CircleCreationComponent({ circleData = null }) {

    const isUpdate = !!circleData
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()
    const [data, setData] = useState({ name: circleData?.name || "", description: circleData?.description || "" })

    function onChangeHandler(e) {
        const { name, value } = e.target
        setData(prev => ({ ...prev, [name]: value }))
    }

    function validateData() {
        let isValid = true
        Object.entries(data).map(([key, value]) => {
            if (!value) {
                toast.warning(key + " must be provided", { toastId: key })
                isValid = false
            }

        })
        return isValid
    }
    async function submitHandler(e) {
        e.preventDefault()
        setIsLoading(true)
        // validating ...
        const isValid = validateData()
        if (!isValid) {
            setIsLoading(false)
            return
        }

        const url = isUpdate ? ("transaction/circle?id=" + circleData?.id) : "transaction/circle"
        const res = await sendRequest(url, { method: isUpdate ? "PUT" : "POST", body: data })
        setIsLoading(false)
        if (!res?.success || res?.err) {

            toast.error(res?.err[0], { toastId: res?.err[0] })
            return
        }

        toast.success(res?.data?.msg)
        router.replace("/circle")
    }
    return (
        <form onSubmit={submitHandler} className="w-full max-w-[400px] flex flex-col items-center mx-auto">

            <ToastContainer position="top-center" theme="dark" />

            {isLoading && <FullPageLoadingComponent />}
            <fieldset className="border-2 p-5 rounded-md">
                <legend className="poppins-bold text-center px-10"> {circleData ? "Update" : "Create"} Circle </legend>
                <div className="my-2 flex flex-col">
                    <label className="my-1 font-medium" htmlFor="name">Name</label>
                    <input placeholder="circle name ..." className="border-none outline-none bg-primary-color h-[45px] rounded-sm pl-2 w-full text-white focus:bg-accent-color focus:text-primary-color font-medium" type="text" name="name" value={data?.name} onChange={onChangeHandler} />
                </div>
                <div className="my-2 flex flex-col w-[350px]">
                    <label className="my-1 font-medium" htmlFor="description">Description</label>
                    <textarea placeholder="circle description ..." className="border-none outline-none bg-primary-color min-h-[80px] focus:bg-accent-color focus:text-primary-color font-medium rounded-sm field-sizing-content p-2 text-white max-h-[200px]" type="text" name="description" value={data?.description} onChange={onChangeHandler} />
                </div>
                <button type="submit" className="bg-accent-color ml-30 mt-2 px-4 py-1 poppins-bold py-1 rounded-sm cursor-pointer">Submit</button>
            </fieldset>

        </form>
    )
}

export default CircleCreationComponent