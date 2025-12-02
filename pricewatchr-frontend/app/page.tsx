import LogoLoader from "@/components/ui/LogoLoader";
import Image from "next/image";

export default function Home() {
  return (
    <main className="flex h-screen items-center justify-center bg-white dark:bg-black">
      <LogoLoader />
    </main>
  );
}
