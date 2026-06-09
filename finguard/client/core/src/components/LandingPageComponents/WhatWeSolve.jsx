import DitchImg from "../../../public/illustrations/ditch.svg"
import CircleImg from "../../../public/illustrations/circle.svg"
import IntellingenceImg from "../../../public/illustrations/intelligence.svg"
import SmartProtectionImg from "../../../public/illustrations/smart-protection.svg"
import AutomationImg from "../../../public/illustrations/automation.svg"
import Image from "next/image"

function WhatWeSolve() {
  const contentArr = [
    {
      "title": "Ditch the Spreadsheets",
      paragraph: "Stop tracking expenses by hand. We automate your transaction records so you can focus on what matters.",
      img:DitchImg
    },
    {
      title: "AI-Powered Security",
      paragraph: "FinGuard AI works in the background to catch suspicious activity the moment it happens.",
      img:AutomationImg
    },
    {
      title: "Smart Transaction Insights",
      paragraph: "We don't just list your spending; we analyze it to give you a clear picture of your financial health.",
      img:SmartProtectionImg
    },
    {
      title: "Advanced Location Intelligence",
      paragraph: 'Using deep analytics, we spot "out of character" transactions by comparing your spending patterns with local trends.',
      img:IntellingenceImg
    },
    {
      title: "The FinGuard Circle",
      paragraph: "Compare your financial habits with the community and see how you rank among your peers.",
      img:CircleImg
    }
  ]
  return (
    <div className="flex flex-col mb-5">
      <h2 className="capitalize poppins-bold text-center text[1.2em] mb-2 text-accent-color">What we solve</h2>

      <section className="flex flex-wrap max-md:flex-col justify-around content-center">

        {contentArr.map(({ title, paragraph,img  }, index) => {
          return <article key={index} className="m-[10px] md:max-w-[42%] bg-off-white flex flex-col p-2 rounded-sm flex-auto shadow-md transition-transform duration-500 hover:border-accent-color hover:border-b-2">
            <h4 className="mb-1 poppins-bold ">  {title} </h4>

            <p>  {paragraph} </p>

            <Image className="self-center my-2" src={img} alt={title} height={200} loading="eager" />
          </article> 
        })}
      </section>
    </div>
  )
}

export default WhatWeSolve