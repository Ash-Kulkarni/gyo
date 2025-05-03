export const setupAudio = () => {

  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  let bgBuffer, bgSource, bgGain;
  async function loadBackgroundLoop() {
    const resp = await fetch('loop.wav');
    const arrayBuf = await resp.arrayBuffer();
    bgBuffer = await audioCtx.decodeAudioData(arrayBuf);
  }
  function playBackgroundLoop() {
    bgSource = audioCtx.createBufferSource();
    bgGain = audioCtx.createGain();
    bgSource.buffer = bgBuffer;
    bgSource.loop = true;
    bgGain.gain.value = 0.8;
    bgSource.connect(bgGain).connect(audioCtx.destination);
    bgSource.start();
  }
  document.addEventListener('click', () => {
    audioCtx.resume().then(() => {
      if (bgBuffer && !bgSource) playBackgroundLoop();
    });
  }, { once: true });
  loadBackgroundLoop();
};
