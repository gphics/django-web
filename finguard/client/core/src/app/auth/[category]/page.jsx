import AuthForm from "@/components/Others/AuthForm"
export async function generateMetadata({ params }) {
  const { category } = await params

  return { title: "Auth: " + category }
}
async function page({ params }) {
  const { category } = await params

  return (
    <main className="flex flex-col text-off-white justify-center items-center mb-1 flex-auto">
      <AuthForm category={category} />
    </main>
  )
}

export default page