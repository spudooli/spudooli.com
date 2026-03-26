import { VideoRTC } from '/driveway/video-rtc.js';
customElements.define('video-rtc', VideoRTC);
const el = document.querySelector('video-rtc');
if (el) el.src = el.getAttribute('src');
