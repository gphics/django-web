import { Poppins} from "next/font/google";
import "./globals.css";
import NavigationComponents from "@/components/NavigationComponents";
import FooterComponent from "@/components/FooterComponent";



const poppins = Poppins({
  weight: [
    "400", //regular

    "700", // bold

    "900" //extrabold
  ],
  subsets: ["latin"],
  variable:"--font-poppins"
})
export const metadata = {
  title: "FinGuard",
  description: "AI driven security & privacy first design",
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className="poppins-regular"
      
    >
      <body className="min-h-screen text-black flex flex-col">
        <NavigationComponents/>
        {children}
        <FooterComponent/>
      </body>
    </html>
  );
}
