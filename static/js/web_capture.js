const WebcamCapture = () => {
    const webcamRef = React.useRef(null);
    const canvasRef = React.useRef(null);
  
    const capture = async () => {
      const imageSrc = webcamRef.current.getScreenshot();
      try {
        const response = await fetch('/process_frame', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: imageSrc }),
        });
        const data = await response.json();
        drawBoxes(data);
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
    const drawBoxes = (faces) => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = '#00FF00';
      ctx.lineWidth = 2;
      ctx.font = '18px Arial';
      ctx.fillStyle = '#00FF00';
  
      faces.forEach(face => {
        const { location, name } = face;
        const [top, right, bottom, left] = location;
        ctx.strokeRect(left, top, right - left, bottom - top);
        ctx.fillText(name, left, top - 5);
      });
    };
  
    React.useEffect(() => {
      const interval = setInterval(() => {
        capture();
      }, 100); // Adjust this value to control frame rate
  
      return () => clearInterval(interval);
    }, []);
  
    return (
      React.createElement('div', { style: { position: 'relative' } },
        React.createElement(Webcam, {
          audio: false,
          ref: webcamRef,
          screenshotFormat: "image/jpeg",
          width: 640,
          height: 480
        }),
        React.createElement('canvas', {
          ref: canvasRef,
          style: {
            position: 'absolute',
            top: 0,
            left: 0,
          },
          width: 640,
          height: 480
        })
      )
    );
  };
  
  ReactDOM.render(React.createElement(WebcamCapture), document.getElementById('react-webcam-container'));
