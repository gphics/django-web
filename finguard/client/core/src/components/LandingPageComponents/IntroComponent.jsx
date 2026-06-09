import Image from "next/image"
import MonitoringImg from "../../../public/illustrations/monitoring.svg"

function IntroComponent() {
  return (
    <div className="flex my-5 max-md:flex-col ">
      <section className="self-center flex flex-col justify-center mb-5 py-2">
        <h2 className="capitalize poppins-bold mb-1 text-[1.2em] text-accent-color">Smart protection that never sleeps.</h2>
        <p>Our AI-driven tools monitor your transactions in real-time to detect anomalies the moment they happen. </p>
      </section>
      <section className="flex justify-center h-full min-w-[58%] md:ml-2">
        <Image className="max-sm:w-[400px]" src={MonitoringImg} alt="monitoring image" width={500} loading="eager" />
      </section>

    </div>
  )
}

export default IntroComponent