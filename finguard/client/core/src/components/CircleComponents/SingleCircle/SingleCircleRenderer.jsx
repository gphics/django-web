"use client"
import { GoHomeFill } from "react-icons/go";
import { BsInfoCircleFill } from "react-icons/bs";
import { RiUserCommunityFill } from "react-icons/ri"
import { FcInvite } from "react-icons/fc";
import { useState } from "react"
import { useRouter } from "next/navigation";

function SingleCircleRenderer({circleId, currentView, isAdmin}) {
    const router = useRouter()

    // Home, Info, Invitation
    const [view, setView] = useState(currentView)
    const navArr = [
        { title: "Home", renderIcon:(props)=> <GoHomeFill {...props}/> },
        { title: "Info", renderIcon: (props) => <BsInfoCircleFill {...props}/> },
     
    ]

    // Admin only route
    if (isAdmin) {
        navArr.push({ title: "Invitation", renderIcon: (props) => <RiUserCommunityFill {...props} /> },)
    }
    
    return (
        <div className="flex flex-col">

            {/* Display Navigation */}
            <section className="flex justify-around items-center bg-primary-color rounded-md w-full max-w-[400px] my-2 self-center h-[60px]">
                {navArr.map(({ title, renderIcon }, i) => {
                    return <div
                        onClick={() => {
                            setView(title)

                            // initiating page reload by appending view
                            router.push("/circle/"+circleId+"?view="+title)
                        }}
                        
                        className={`flex flex-col justify-center items-center cursor-pointer text-[.8em] transition-all duration-400 hover:text-accent-color hover:poppins-bold ${title === view ?"text-accent-color":"text-white"}`} key={i}>
                       {renderIcon({size:20})}
                        <h4>{title}</h4>
                    </div>
                })}
            </section>


        </div>
    )
}

export default SingleCircleRenderer