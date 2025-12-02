const SvgLoader = ({ size = 100, color = "#3b82f6" }) => (
  <svg
    className="svg-spinner-fallback"
    width={size}
    height={size}
    viewBox="0 0 50 50"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle
      cx="25"
      cy="25"
      r="20"
      fill="none"
      strokeWidth="5"
      stroke={color}
      strokeOpacity="0.3"
    />
    <path
      d="M 25 5 A 20 20 0 0 1 45 25"
      fill="none"
      strokeWidth="5"
      stroke={color}
    >
      {/* This is the animation element for the spinning effect.
        It rotates the entire path element for 1 second continuously.
      */}
      <animateTransform
        attributeName="transform"
        attributeType="XML"
        type="rotate"
        from="0 25 25"
        to="360 25 25"
        dur="1s"
        repeatCount="indefinite"
      />
    </path>
  </svg>
);

export default SvgLoader;
