"use client"

import FullPageLoadingComponent from "@/components/Others/FullPageLoadingComponent"
import MediaPresentationComponent from "@/components/Others/MediaPresentationComponent"
import sendRequest from "@/utils/requestSender"
import { useParams, useRouter } from "next/navigation"
import { useState} from "react"
import { FaSearch } from "react-icons/fa"
import { toast, ToastContainer } from "react-toastify"

function MemberInvitationClientComponent() {
    const { id: circleId } = useParams()
    const [username, setUsername] = useState("")
    const [users, setUsers] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()
  

    /**
     * This function fetches users with matching username
     * @param {Event} e 
     * @returns {Array | null}
     */
    async function submitHandler(e) {
        e.preventDefault()
       
        if (!username) {
            toast.warning("Username must be provided")
            return
        }
        setIsLoading(true)
        const url = "account/profile?search=" + username
        const res = await sendRequest(url)
        setIsLoading(false)
        if (!res?.success || res?.err) {
            toast.error(res?.err[0])
            return
        }

        const usersList = res?.data?.msg || []
        const data = usersList.map(elem => {
            const builtData = {
                id: elem?.user?.id,
                media: elem?.media,
                username: elem?.user?.username,
            }
            return builtData
        })
        

        // if no user found
        if (!data?.length) {
            toast.info("Matching user does not exist")
        }
        setUsers(data)


    }

    async function sendInvitation(id) {
        setIsLoading(true)
        const url = "transaction/circle-invite"
        const body = {
            circle: circleId,
            user: id
        }
        const res = await sendRequest(url, { body, method: "POST" })
        setIsLoading(false)
        if (!res?.success || res?.err?.[0]) {
            toast.error(res?.err[0], { toastId: id })
            return
        }

        toast.success(res?.data?.msg, { toastId: id })
        
        router.refresh()
        
        // performing a full page reload to replace stale circle invites.
        // setTimeout(() => { window.location.reload() }, 3000)

    }
    return (
        <div className="my-2 flex flex-col">
            {!!isLoading && <FullPageLoadingComponent />}
            <ToastContainer theme="dark" position="top-center" />
            <form onSubmit={submitHandler} className="my-2 mx-auto">
                <h3 className="poppins-bold uppercase text-center my-1">Invite to collaborate</h3>


                <div className="mt-2 w-[350px] flex justify-between items-center">
                    <input type="search" name="username" placeholder="username ..." className="bg-accent-color flex-auto h-[45px] pl-2 rounded-l-md outline-none border-none" onChange={(e) => setUsername(e.target.value)} value={username} />
                    <button type="submit" className="ml-1 bg-accent-color text-center h-[45px] px-3 rounded-r-md cursor-pointer" >
                        <FaSearch />
                    </button>
                </div>
            </form>

            {/* Displaying users */}
            {!!users.length &&
                <section className="flex flex-wrap justify-around items-center">
                    {users.map((elem, i) => {
                        return <article key={i} className="flex justify-between w-full max-w-[300px] my-2 bg-overlay p-3 items-center hover:text-white hover:bg-primary-color">
                            <MediaPresentationComponent name={elem?.username} media={elem?.user_media} />

                            <div className="flex flex-col flex-auto ml-3">
                                <h4 className="capitalize poppins-bold"> {elem?.username}  </h4>
                                <button className="bg-accent-color px-4 py-2 cursor-pointer rounded-sm poppins-bold" onClick={() => sendInvitation(elem?.id)} type="button">Invite</button>
                            </div>

                        </article>
                    })}


                </section>
            }

            
        </div>
    )
}

export default MemberInvitationClientComponent