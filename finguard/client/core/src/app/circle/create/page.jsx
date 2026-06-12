import CircleCreationComponent from "@/components/CircleComponents/CircleCreationComponent"


export async function generateMetadata({ searchParams }) {

    const { id } = await searchParams
    return {
        title: id ? ("Update Circle" + id) : "Create Circle"
    }
}

async function page({ searchParams }) {
    const { id } = await searchParams
    return (
        <div className="flex-auto flex flex-col px-1">
            <CircleCreationComponent/>
        </div>
    )
}

export default page