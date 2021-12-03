var YooniKFaceAuthenticationSDK = (function(){

    let width = 640;
    let height = 480;
    let output = null;
    let camera = null;

    async function authenticateWithFace(event) {
        event.preventDefault();
        document.getElementById('yk-content').innerHTML = '<div class="spinner-grow text-info" role="status"><span class="sr-only">Loading...</span></div>';
        const context = output.getContext('2d');
        context.drawImage(camera, 0, 0, width, height);
        const imageData = output.toDataURL("image/png");
        let formData = new FormData(event.target) // event.target is the form
        formData.append('user_selfie', imageData);
        fetch(event.target.action, {
            method: 'POST',
            body: formData
        }).then((resp) => {
            if (resp.ok) {
                return resp.json();
            } else {
                return resp.text();
            }
        }).then((data) => {
            document.getElementById('yk-content').innerHTML = data.html !== undefined ? data.html : data;
        }).catch((err) => {
            document.getElementById('yk-content').innerHTML = err;
        });
    }

    function main() {
        console.log("Initializing video")

        if(screen.availHeight > screen.availWidth){
            const temp = height;
            height = width;
            width = temp;
        }
        output = document.getElementById('output');
        output.setAttribute("width", width);
        output.setAttribute("height", height);
        camera = document.getElementById("camera");
        camera.setAttribute("width", width);
        camera.setAttribute("height", height);

        // Get a permission from user to use a camera.
        if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("Sorry, your webcam is unavailable to take a photo");
            return;
        }
        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        })
        .then(function(stream) {
            camera.srcObject = stream;
            camera.onloadedmetadata = function(e) {
                camera.play();
            };
        })
        .catch(function(err) {
            alert("Sorry, camera permissions are needed for face authentication.");
        });
    }

    window.addEventListener('load', (event) => {
        const faceAuthenticationForm = document.getElementById( "face-authentication-form" );
        faceAuthenticationForm.addEventListener('submit', authenticateWithFace);

        main();
    });

})();