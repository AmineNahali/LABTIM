'use strict';

/* global THREE */

function mainXYZ(bl1,bl2) {
  const canvas = document.querySelector('#c');
  const renderer = new THREE.WebGLRenderer({canvas});
  renderer.shadowMap.enabled = true;

  const fov = 50;
  const aspect = 2;  // the canvas default
  const near = 0.1;
  const far = 5000;
  const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
  const pntlight = new THREE.PointLight(0xffffff, 2);
  camera.position.set(0, 150, 250);
  camera.add(pntlight);

  const controls = new THREE.OrbitControls(camera, canvas);
  controls.target.set(0, 5, 0);
  controls.update();

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('lightgrey');
  const mtt = new THREE.MeshStandardMaterial({ color: 0xf7372d });
  const mtt2 = new THREE.MeshStandardMaterial({ color: 0xac50e1,opacity: 0.5,transparent: true});
  
  
  mtt.flatShading = true;
  for(var i=0; i<mtt.length; i++){
    mtt[i].flatShading = true;
  }


  {
    const planeSize = 0;

    const loader = new THREE.TextureLoader();
    //const texture = loader.load('https://r105.threejsfundamentals.org/threejs/resources/images/checker.png');
    //texture.wrapS = THREE.RepeatWrapping;
    //texture.wrapT = THREE.RepeatWrapping;
    //texture.magFilter = THREE.NearestFilter;
    const repeats = planeSize / 2;
    //texture.repeat.set(repeats, repeats);

    const planeGeo = new THREE.PlaneBufferGeometry(planeSize, planeSize);
    
    const planeMat = new THREE.MeshPhongMaterial({
     /* map: texture*,* */
      side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(planeGeo, planeMat);
    mesh.rotation.x = Math.PI * -.5;
    

    scene.add(mesh);
  }

  {
    const color = 0xFFFFFF;
    const intensity = 1;
    const light = new THREE.DirectionalLight(color, intensity);
    light.position.set(0, 600, 600);
    const light2 = new THREE.DirectionalLight(color, intensity);
    light2.position.set(0, -600, -600);
    scene.add(light);
    scene.add(light.target);
    scene.add(light2);
    scene.add(light2.target);
  }
  {
    //const light = new THREE.AmbientLight(0xffffff); // soft white light
    //scene.add(light);
    scene.add(new THREE.HemisphereLight(0xffffff,0xffffff,1.0));
  }

 /* {
    const objLoader = new THREE.OBJLoader2();
    
    objLoader.load(bl, (event) => {
      const root = event.detail.loaderRootNode;
      root.material = new THREE.MeshStandardMaterial({ color: 0xffff00 })
      scene.add(root);
      root.position.set(-64, -256, -256);
    });
  }*/
  {
    const objLoader = new THREE.OBJLoader2();
    const objLoader2 = new THREE.OBJLoader2();
    objLoader.load(bl1,(event)=>{
      const root = event.detail.loaderRootNode;
      scene.add(root);
      root.position.set(-64, -256, -256);
      root.traverse( function ( child ) {
        if ( child instanceof THREE.Mesh ) {
          child.material = mtt;
        }
      });
      //scene.overrideMaterial = mtt;
    });
    objLoader2.load(bl2,(event)=>{
      const root2 = event.detail.loaderRootNode;
      scene.add(root2);
      root2.position.set(-64, -256, -256);
      root2.traverse( function ( child2 ) {
        if ( child2 instanceof THREE.Mesh ) {
          child2.material = mtt2;
        }
      });

    });
  }

  function resizeRendererToDisplaySize(renderer) {
    const canvas = renderer.domElement;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    const needResize = canvas.width !== width || canvas.height !== height;
    if (needResize) {
      renderer.setSize(width, height, false);
    }
    return needResize;
  }

  function render() {

    if (resizeRendererToDisplaySize(renderer)) {
      const canvas = renderer.domElement;
      camera.aspect = canvas.clientWidth / canvas.clientHeight;
      camera.updateProjectionMatrix();
    }

    renderer.render(scene, camera);

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
}
