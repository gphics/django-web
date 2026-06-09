import DataInputImg from "../../../public/illustrations/data-input.svg"
import AutomationImg from "../../../public/illustrations/automation.svg"
import ReportImg from "../../../public/illustrations/report.svg"
import Image from "next/image"
import Link from "next/link"

function HowItWorks() {
  const contentArr = [
    {
      step: "Input Your Data",
      process: "Manually upload your transaction details through our secure, streamlined form. You’re in total control of the data you share—no bank logins or third-party connections required.",
      img: DataInputImg
    },
    {
      step: "AI Analysis",
      process: "The moment you hit submit, the FinGuard AI engine goes to work. It cross-references your entry against your historical patterns and local spending data to identify inconsistencies.",
      img: AutomationImg
    },
    {
      step: "Get Your Report",
      process: "Instantly view your transaction health. Whether it’s a green light for a normal transaction or a red flag for a detected anomaly, you’ll get the insights you need to stay protected.",
      img: ReportImg
    },
  ]
  return (
    <div className="flex flex-col my-2">
      <h2 className='text-center text-accent-color poppins-bold capitalize mb-1'>How it works</h2>
      <section className="flex flex-wrap max-md:flex-col justify-around">
        {contentArr.map(({ step, process, img }, index) => {
          return <article key={index} className="shadow-md bg-off-white m-[10px] rounded-sm flex flex-col p-2 md:max-w-[42%] hover:border-accent-color hover:border-b-2 flex-auto">
            <h3 className="poppins-bold">{index + 1}. {step}</h3>
            <p>  {process} </p>
            <Image className="self-center my-2" src={img} alt={step} height={200} loading="eager" />
          </article>
        })}
      </section>
      <article className="my-2 bg-primary-color rounded-sm flex flex-col text-off-white">
        <h3 className="text-center text-[1.2em] poppins-bold">Total Data Oversight</h3>
        <p className="p-1 text-center">We prioritize your privacy by skipping third-party bank connections. You manually manage what you share, ensuring your credentials never leave your sight.</p>

        <Link href="/auth/register" className="self-center bg-accent-color my-2 text-off-white rounded-sm py-2 px-3 hover:text-primary-color poppins-bold"> Get Started </Link>
      </article>
    </div>
  )
}

export default HowItWorks