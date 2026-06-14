"use client"

import { useState } from "react"
import { toast, ToastContainer } from "react-toastify"
import FullPageLoadingComponent from "./FullPageLoadingComponent"
import CookieManager from "@/utils/cookieManager"

function MediaUploadComponent({ id, type }) {
const [isLoading, setIsLoading] = useState(false)
    const [file, setFile] = useState(null)
    const cookieMgt = CookieManager()
    const authToken = cookieMgt.getCookie()
    const acceptable_mimetypes = [
        "image/png",
        "image/jpg",
        "image/jpeg",
        "image/gif",
        "image/webp",
        "image/svg+xml",
        "image/svg",
    ].toString()
    
    async function uploadFile(e) {
        e.preventDefault()
        if (!file) {
            toast.warning("Image file must be provided")
            return
        }
        setIsLoading(true)
        let url = process.env.NEXT_PUBLIC_SERVER_URL +"media/"
        if (type === "circle") {
            url = url + "?id="+id
        }
        const method = "POST"

        const formData = new FormData()
        formData.append("media", file)

        const first = await fetch(url, { method, body: formData, headers: { Authorization: "Token " + authToken } })
        const second = await first.json()

        setIsLoading(false)
        
        if (second?.err || !second?.success) {
            toast.error(String(second?.err?.msg))

            return
        }
        toast.success(second?.data?.msg)
    }
    return (
        <form onSubmit={uploadFile} className="w-full max-w-[400px]">
            {!!isLoading && <FullPageLoadingComponent/>}
            <ToastContainer theme="dark" position="top-center" />
            
            <fieldset className="flex flex-col items-center border-2 rounded-md">
                <legend className="text-center px-10 ">Media</legend>
                <input className="bg-primary-color text-white h-[45px] pt-2 px-2 mt-2 cursor-pointer focus:text-primary-color focus:bg-accent-color border-none outline-none rounded-md mx-auto" type="file" name="media" accept={acceptable_mimetypes} onChange={(e) => {
                    setFile(e.target.files[0])
                }} />
                <button className="px-5 py-2 font-medium cursor-pointer my-2 rounded-md bg-accent-color w-fit" type="submit">Submit</button >
            </fieldset>

        </form>
    )
}

export default MediaUploadComponent