import LandingPageComponentsArr from "@/components/LandingPageComponents"

export async function generateMetadata() {
  return {title:"Welcome To Finguard"}
}



function page() {
  

  return (
    <main className="flex flex-col p-2">
      {LandingPageComponentsArr.map((Component, index) => <Component key={index} />)}
    </main>
  )
}

export default page