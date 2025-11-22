/**
 * Checks if the current device is a desktop (non-touch device)
 * This is more reliable than checking window width alone
 */
export const isDesktop = (): boolean => {
  // Check if touch is not supported
  const hasNoTouch = !('ontouchstart' in window || navigator.maxTouchPoints > 0);
  
  // Check if it's not a mobile user agent
  const isNotMobile = !/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  // A device is considered desktop if it has no touch AND is not a mobile user agent
  return hasNoTouch && isNotMobile;
};
