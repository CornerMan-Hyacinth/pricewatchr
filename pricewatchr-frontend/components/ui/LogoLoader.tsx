import SvgLoader from "./SvgLoader"; // Import the new component

const LogoLoader = () => {
  const spinnerSize = 120; // Define size once for both video and fallback

  return (
    <div className="spinner-container">
      <video
        className="spinning-logo"
        width={spinnerSize}
        height={spinnerSize}
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
      >
        {/* Primary Content: The MP4 video source */}
        <source src="/videos/pricewatchr_logo_animation.mp4" type="video/mp4" />

        {/* 🌟 Visual Fallback: The pure SVG Spinner 🌟 */}
        <SvgLoader size={spinnerSize} />
      </video>
    </div>
  );
};

export default LogoLoader;
