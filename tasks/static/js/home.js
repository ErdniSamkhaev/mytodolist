let scene, camera, renderer, cube, raycaster, mouse;
let cubes = []; // Массив для хранения мелких кубиков
let isExploded = false; // Флаг, указывающий на то, что куб рассыпался

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({color: 0x00ff00});
    cube = new THREE.Mesh(geometry, material);
    cube.rotationSpeed = new THREE.Vector3(0.01, 0.01, 0); // Скорость вращения большого куба
    scene.add(cube);

    camera.position.z = 5;

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    document.addEventListener('mousemove', onDocumentMouseMove, false);
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

function onDocumentMouseMove(event) {
    event.preventDefault();

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(scene.children);

    if (intersects.length > 0 && !isExploded) {
        explodeCube(); // Вызываем функцию взрыва куба
    }
}

function explodeCube() {
    isExploded = true;
    scene.remove(cube); // Удаляем большой куб из сцены

    // Создаем мелкие кубики с увеличенным размером
    for (let i = 0; i < 10; i++) {
        const geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5); // Увеличенный размер мелких кубиков
        const material = new THREE.MeshBasicMaterial({color: Math.random() * 0xffffff});
        const smallCube = new THREE.Mesh(geometry, material);

        // Позиционируем мелкие кубики там, где был большой куб
        smallCube.position.copy(cube.position);

        // Даем каждому мелкому кубику случайную скорость и скорость вращения
        smallCube.velocity = new THREE.Vector3(
            (Math.random() - 0.5) * 0.2, // Уменьшаем скорость для более медленного движения
            (Math.random() - 0.5) * 0.2,
            (Math.random() - 0.5) * 0.2
        );
        smallCube.rotationSpeed = new THREE.Vector3(
            Math.random() * 0.1, // Случайная скорость вращения
            Math.random() * 0.1,
            Math.random() * 0.1
        );

        scene.add(smallCube);
        cubes.push(smallCube);
    }
}


function animate() {
    requestAnimationFrame(animate);

    if (!isExploded) {
        // Вращаем большой куб
        cube.rotation.x += cube.rotationSpeed.x;
        cube.rotation.y += cube.rotationSpeed.y;
    } else {
        // Обновляем позиции и вращение мелких кубиков
        cubes.forEach((smallCube) => {
            smallCube.position.add(smallCube.velocity);
            smallCube.rotation.x += smallCube.rotationSpeed.x;
            smallCube.rotation.y += smallCube.rotationSpeed.y;
            smallCube.rotation.z += smallCube.rotationSpeed.z;
            checkBounds(smallCube);
        });
    }

    renderer.render(scene, camera);
}

function checkBounds(smallCube) {
    const bounds = 5; // Пределы сцены

    // Проверяем столкновения с границами для мелкого кубика
    ['x', 'y', 'z'].forEach((axis) => {
        if (Math.abs(smallCube.position[axis]) > bounds) {
            smallCube.velocity[axis] = -smallCube.velocity[axis];
            smallCube.position[axis] = Math.sign(smallCube.position[axis]) * bounds;
        }
    });
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

init();
