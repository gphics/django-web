"use client"

import FullPageLoadingComponent from "@/components/Others/FullPageLoadingComponent"
import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"
import { useRouter } from "next/navigation"
import { useState } from "react"

import { toast, ToastContainer } from "react-toastify"

function InfoMemberComponent({ circleId, members, isAdmin, authUserId }) {
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()
    const memberArr = members.map(elem => {
        const obj = {
            role: elem?.role,
            userId: elem?.user.id,
            username: elem?.user.username,
            media: elem?.user.profile.media,
            joinedAt: elem?.joined_at
        }
        return obj
    })

    async function removeCircleMember(userId) {
        setIsLoading(true)
        const url = "transaction/remove-circle-member/" + circleId + "?user=" + userId
        const method = "DELETE"

        const res = await sendRequest(url, { method })
        setIsLoading(false)
        if (!res?.success || res?.err) {
            toast.error(res?.err?.[0])
            return
        }
        router.refresh()
    }

    async function leaveCircle() {
        setIsLoading(true)
        const url = "transaction/leave-circle/" + circleId
        const method = "DELETE"

        const res = await sendRequest(url, { method })
        console.log(res)
        setIsLoading(false)
        if (!res?.success || res?.err) {
            toast.error(res?.err?.[0])
            return
        }
        router.replace("/circle")

    }
    return (
        <div>
            {!!isLoading && <FullPageLoadingComponent />}
            <ToastContainer />
            <h3 className="text-center my-2 poppins-bold">Members({memberArr.length})   </h3>
            {memberArr.map((elem, i) => {
                return <section key={i} className={`my-2 hover:bg-primary-color hover:text-white shadow-md w-full max-w-[400px] p-2 ${authUserId === elem?.userId ? "bg-primary-color text-white": "bg-white"} `}>

                    <div className="flex items-center my-1 ">
                        <MediaPresentationComponent name={elem?.username} media={elem?.media} />
                        <h3 className="ml-4 capitalize font-semibold"> {elem?.username} </h3>
                    </div>

                    <small className="my-1 poppins-bold"> {elem?.role}  </small>

                    {/* Actions */}
                    <div className="flex justify-between">
                        {isAdmin && authUserId !== elem?.userId && <button className="px-7 py-1 bg-accent-color  text-white cursor-pointer hover:poppins-bold transition-all duration-400" onClick={() => removeCircleMember(elem?.userId)} type="button">Remove</button>}

                        {elem?.userId === authUserId &&
                            <button className="px-7 py-1 bg-accent-color  text-white cursor-pointer hover:poppins-bold transition-all duration-400" onClick={() => leaveCircle()} type="button">Leave</button>
                        }
                    </div>

                </section>
            })}
        </div>
    )
}

export default InfoMemberComponent