import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const colors = new Uint8Array(3);
colors[0] = 0;
colors[1] = 128;
colors[2] = 255;

const gradientMap = new THREE.DataTexture(colors, 3, 1, THREE.RedFormat);
gradientMap.needsUpdate = true;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

scene.background = new THREE.Color(0x1a2138);
const DARK_GRAY = 0x333333;
const LIGHT_GRAY = 0x888888;
const DARK_GROUND = 0x212a32;

const FUSELAGE_DEFAULT_COLOR = 0xffffff;    
const WING_DEFAULT_COLOR = 0xb0b0b0;       
const ENGINE_BODY_DEFAULT_COLOR = 0x333333;  

const CRITICAL_COLOR = new THREE.Color(0xff4444);
const WARNING_COLOR = new THREE.Color(0xffaa00);
const NORMAL_COLOR = new THREE.Color(0x44ff44); 

const FLAP_WING_Z_POSITION = 0.8;

let currentRPM = 0;
const labelsContainer = document.getElementById('labels-container');
const labelMeshes = [];

let labelsVisible = true;

const rpmHistory = [];
const maxHistoryPoints = 50; 

camera.aspect = window.innerWidth / window.innerHeight;
camera.updateProjectionMatrix();
camera.position.set(0, 3, 10);
const controls = new OrbitControls(camera, renderer.domElement);
controls.update();
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 10, 5).normalize();
scene.add(directionalLight);

const gridSize = 10;
const divisions = 40;
const gridColor = DARK_GRAY;
const centerLineColor = LIGHT_GRAY;
const gridHelper = new THREE.GridHelper(gridSize, divisions, centerLineColor, gridColor);
gridHelper.position.y = -2;
scene.add(gridHelper);

const basePlaneGeometry = new THREE.PlaneGeometry(gridSize, gridSize);
const basePlaneMaterial = new THREE.MeshStandardMaterial({ color: DARK_GROUND, side: THREE.DoubleSide });
const basePlane = new THREE.Mesh(basePlaneGeometry, basePlaneMaterial);
basePlane.rotation.x = Math.PI / 2;
basePlane.position.y = -2.01;
scene.add(basePlane);

const airplaneGroup = new THREE.Group();
airplaneGroup.position.y = 0;

const fuselageMaterial = new THREE.MeshToonMaterial({ color: FUSELAGE_DEFAULT_COLOR, gradientMap: gradientMap });
const wingMaterial = new THREE.MeshToonMaterial({ color: WING_DEFAULT_COLOR, gradientMap: gradientMap });
const flapMaterial = new THREE.MeshToonMaterial({ color: 0x888888, gradientMap: gradientMap });
const tailVerticalMaterial = new THREE.MeshToonMaterial({ color: FUSELAGE_DEFAULT_COLOR, gradientMap: gradientMap });
const tailHorizontalMaterial = new THREE.MeshToonMaterial({ color: WING_DEFAULT_COLOR, gradientMap: gradientMap });

const fuselageGeometry = new THREE.CylinderGeometry(0.8, 0.8, 6, 32);
const fuselage = new THREE.Mesh(fuselageGeometry, fuselageMaterial);
fuselage.rotation.x = Math.PI / 2;
fuselage.name = 'fuselage';
airplaneGroup.add(fuselage);

const wingGeometry = new THREE.BoxGeometry(8, 0.2, 2);
const wing = new THREE.Mesh(wingGeometry, wingMaterial);
wing.position.z = 0;
wing.name = 'wing';
airplaneGroup.add(wing);

const flapWidth = 2.5;
const flapHeight = 0.15;
const flapDepth = 0.8;

const flapLeftGeometry = new THREE.BoxGeometry(flapWidth, flapHeight, flapDepth);
const flapRightGeometry = new THREE.BoxGeometry(flapWidth, flapHeight, flapDepth);

const flapLeft = new THREE.Mesh(flapLeftGeometry, flapMaterial);
flapLeft.name = 'flapLeft';
flapLeft.geometry.translate(flapWidth / 2, 0, 0);
flapLeft.position.set(-2.5, 0, FLAP_WING_Z_POSITION);
airplaneGroup.add(flapLeft);

const flapRight = new THREE.Mesh(flapRightGeometry, flapMaterial);
flapRight.name = 'flapRight';
flapRight.geometry.translate(-flapWidth / 2, 0, 0);
flapRight.position.set(2.5, 0, FLAP_WING_Z_POSITION);
airplaneGroup.add(flapRight);

const tailVerticalGeometry = new THREE.BoxGeometry(0.2, 2, 2);
const tailVertical = new THREE.Mesh(tailVerticalGeometry, tailVerticalMaterial);
tailVertical.position.set(0, 1.2, -3);
airplaneGroup.add(tailVertical);

const tailHorizontalGeometry = new THREE.BoxGeometry(3, 0.2, 1);
const tailHorizontal = new THREE.Mesh(tailHorizontalGeometry, tailHorizontalMaterial);
tailHorizontal.position.set(0, 0.5, -3);
tailHorizontal.name = 'tailHorizontal';
airplaneGroup.add(tailHorizontal);

function createEngine() {
    const engineGroup = new THREE.Group();
    const engineMaterial = new THREE.MeshToonMaterial({ color: ENGINE_BODY_DEFAULT_COLOR, gradientMap: gradientMap });

    const bodyGeometry = new THREE.CylinderGeometry(0.6, 0.5, 2.5, 32);
    const bodyMesh = new THREE.Mesh(bodyGeometry, engineMaterial);
    bodyMesh.rotation.x = Math.PI / 2;
    engineGroup.add(bodyMesh);

    const intakeRingGeometry = new THREE.TorusGeometry(0.5, 0.1, 16, 100);
    const intakeRingMaterial = new THREE.MeshToonMaterial({ color: 0x333333, gradientMap: gradientMap });
    const intakeRingMesh = new THREE.Mesh(intakeRingGeometry, intakeRingMaterial);
    intakeRingMesh.rotation.x = Math.PI / 2;
    intakeRingMesh.position.z = 1.25;
    engineGroup.add(intakeRingMesh);

    const fanGeometry = new THREE.CylinderGeometry(0.4, 0.4, 0.1, 32);
    const fanMaterial = new THREE.MeshToonMaterial({ color: 0x666666, gradientMap: gradientMap });
    const fanMesh = new THREE.Mesh(fanGeometry, fanMaterial);
    fanMesh.rotation.x = Math.PI / 2;
    fanMesh.position.z = 1.35;
    fanMesh.name = 'fan';
    engineGroup.add(fanMesh);

    return engineGroup;
}

const engineLeft = createEngine();
engineLeft.position.set(-3.5, 0, 0);
engineLeft.name = 'engineN1';
airplaneGroup.add(engineLeft);

const engineRight = createEngine();
engineRight.position.set(3.5, 0, 0);
engineRight.name = 'engineN2';
airplaneGroup.add(engineRight);

function createDemarcationLabel(text, position, id) {
    const referenceObject = new THREE.Object3D();
    referenceObject.position.copy(position);
    airplaneGroup.add(referenceObject);

    const labelDiv = document.createElement('div');
    labelDiv.className = 'demarcation-label';
    labelDiv.textContent = text;
    labelDiv.id = id;
    labelsContainer.appendChild(labelDiv);

    labelMeshes.push({ mesh: referenceObject, element: labelDiv });
}

createDemarcationLabel("MOTOR N1", new THREE.Vector3(-3.5, 0.7, 0), "label-motor-n1");
createDemarcationLabel("MOTOR N2", new THREE.Vector3(3.5, 0.7, 0), "label-motor-n2");
createDemarcationLabel("ASA/HIDRÁULICO", new THREE.Vector3(0, 0.5, FLAP_WING_Z_POSITION + 0.5), "label-wing-system");
createDemarcationLabel("FUSELAGEM/ELÉTRICO", new THREE.Vector3(0, 1.5, 0), "label-fuselage-system");


scene.add(airplaneGroup);

const systemLabelMap = {
    'MOTOR': 'engine', 'PROPULSÃO': 'engine',
    'ASA': 'wing', 'COMBUSTÍVEL': 'wing', 'ESTRUTURAL': 'wing',
    'HIDRÁULICO': 'wing',
    'ESTRUTURA': 'fuselage',
    'FUSILAGEM': 'fuselage',
    'ELETRICO': 'fuselage', 'AVIONICS': 'fuselage', 'FUSELAGEM': 'fuselage',
};

function getSeverityColor(severity) {
    const severityColorMap = {
        'CRITICAL': CRITICAL_COLOR,
        'WARNING': WARNING_COLOR,
        'NORMAL': new THREE.Color(0xAAAAAA),
        'DEFAULT': new THREE.Color(0xAAAAAA)
    };
    return severity.toUpperCase() === 'NORMAL' ? NORMAL_COLOR : severityColorMap[severity.toUpperCase()] || severityColorMap['DEFAULT'];
}

function applyHierarchicalFeedback(data, airplaneGroup) {

    const {
        overall_severity: overallSeverity = 'NORMAL',
        faults = []
    } = data.airplane;

    const isFault = overallSeverity !== 'NORMAL';
    const severityOrder = { 'CRITICAL': 3, 'WARNING': 2, 'NORMAL': 1, 'DEFAULT': 1 };
    
    const fuselageMesh = airplaneGroup.getObjectByName('fuselage');
    const wingMesh = airplaneGroup.getObjectByName('wing');
    const engineN1Mesh = airplaneGroup.getObjectByName('engineN1');
    const engineN2Mesh = airplaneGroup.getObjectByName('engineN2');
    const flapLeftMesh = airplaneGroup.getObjectByName('flapLeft');
    const flapRightMesh = airplaneGroup.getObjectByName('flapRight');

    if (fuselageMesh) fuselageMesh.material.color.set(new THREE.Color(FUSELAGE_DEFAULT_COLOR));
    if (wingMesh) wingMesh.material.color.set(new THREE.Color(WING_DEFAULT_COLOR));
    if (flapLeftMesh) flapLeftMesh.material.color.set(new THREE.Color(0x888888));
    if (flapRightMesh) flapRightMesh.material.color.set(new THREE.Color(0x888888));
    
    const defaultEngineColor = new THREE.Color(ENGINE_BODY_DEFAULT_COLOR);
    if (engineN1Mesh && engineN1Mesh.children.length > 0) engineN1Mesh.children[0].material.color.set(defaultEngineColor);
    if (engineN2Mesh && engineN2Mesh.children.length > 0) engineN2Mesh.children[0].material.color.set(defaultEngineColor);

    document.querySelectorAll('.demarcation-label').forEach(label => {
        label.classList.remove('label-critical', 'label-warning');
        label.style.display = labelsVisible ? 'block' : 'none'; 
    });

    const panel = document.getElementById('diagnostic-panel');
    const panelSeverity = document.getElementById('panel-severity');
    const faultsList = document.getElementById('faults-list'); 

    if (!panel || !panelSeverity || !faultsList) {
        console.error("Erro: Um ou mais elementos do painel de diagnóstico não foram encontrados no DOM.");
        return; 
    }
    
    faultsList.innerHTML = ''; 

    if (isFault) {
        panel.classList.add('visible');
        panelSeverity.textContent = `STATUS: ${overallSeverity}`;
        panelSeverity.style.color = getSeverityColor(overallSeverity).getStyle();

        const activeFaults = faults.filter(f => (f.severity || 'NORMAL').toUpperCase() !== 'NORMAL');

        if (activeFaults.length > 0) {
             activeFaults.forEach((fault, index) => {
                const severityText = (fault.severity || 'NORMAL').toUpperCase();
                const faultColor = getSeverityColor(severityText); 
                
                const faultDiv = document.createElement('div');
                faultDiv.className = 'fault-detail';
                faultDiv.style.borderLeft = `4px solid ${faultColor.getStyle()}`;
                
                const title = document.createElement('strong');
                title.textContent = `${index + 1}. ${fault.n1_system || 'SISTEMA INDEFINIDO'}`;
                faultDiv.appendChild(title);

                const subsystem = document.createElement('p');
                subsystem.innerHTML = `Subsistema: ${fault.n2_subsystem || 'N/A'}`;
                faultDiv.appendChild(subsystem);

                const detail = document.createElement('p');
                detail.innerHTML = `Falha: ${fault.n3_fault || 'N/A'}`;
                faultDiv.appendChild(detail);
                
                const severityP = document.createElement('p');
                severityP.innerHTML = `Severidade: <span style="color: ${faultColor.getStyle()}; font-weight: bold;">${severityText}</span>`;
                faultDiv.appendChild(severityP);

                faultsList.appendChild(faultDiv);
             });
        } else {
             faultsList.innerHTML = '<p>Falha geral detectada, mas detalhes indisponíveis.</p>';
        }

    } else {
        panel.classList.remove('visible');
        faultsList.innerHTML = '<p>Nenhuma falha detectada.</p>';
        return; 
    }

    const componentSeverity = { 'engine': 'NORMAL', 'wing': 'NORMAL', 'fuselage': 'NORMAL' };
    
    faults.forEach(fault => {
        const system = (fault.n1_system || '').toUpperCase();
        const component = systemLabelMap[system];
        const currentFaultSeverity = (fault.severity || 'NORMAL').toUpperCase();
        
        if (component) {
            const currentMaxSeverity = componentSeverity[component];
            if (severityOrder[currentFaultSeverity] > severityOrder[currentMaxSeverity]) {
                componentSeverity[component] = currentFaultSeverity;
            }
        }
    });


    for (const component in componentSeverity) {
        const severity = componentSeverity[component];
        if (severity === 'NORMAL') continue; 

        const color = severity === 'CRITICAL' ? CRITICAL_COLOR : WARNING_COLOR;
        const severityClass = severity === 'CRITICAL' ? 'label-critical' : 'label-warning';

        if (component === 'engine') {
            if (engineN1Mesh && engineN1Mesh.children.length > 0) engineN1Mesh.children[0].material.color.set(color);
            if (engineN2Mesh && engineN2Mesh.children.length > 0) engineN2Mesh.children[0].material.color.set(color);
            document.getElementById('label-motor-n1').classList.add(severityClass);
            document.getElementById('label-motor-n2').classList.add(severityClass);
            
        } else if (component === 'wing') {
            if (wingMesh) wingMesh.material.color.set(color);
            if (flapLeftMesh) flapLeftMesh.material.color.set(color);
            if (flapRightMesh) flapRightMesh.material.color.set(color);
            document.getElementById('label-wing-system').classList.add(severityClass);
            
        } else if (component === 'fuselage') {
            if (fuselageMesh) fuselageMesh.material.color.set(color);
            document.getElementById('label-fuselage-system').classList.add(severityClass);
        }
    }
}

function updateRPMChart(newRPM) {
    const canvas = document.getElementById('rpm-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    rpmHistory.push(newRPM);
    if (rpmHistory.length > maxHistoryPoints) {
        rpmHistory.shift();
    }

    ctx.clearRect(0, 0, width, height);

    ctx.strokeStyle = '#444';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height / 2); 
    ctx.lineTo(width, height / 2);
    ctx.stroke();

    ctx.strokeStyle = '#00bcd4'; 
    ctx.lineWidth = 2;
    ctx.beginPath();

    const maxRPM = 3000;
    const stepX = width / (maxHistoryPoints - 1);

    for (let i = 0; i < rpmHistory.length; i++) {
        const val = rpmHistory[i];
        const y = height - (val / maxRPM) * height; 
        const x = i * stepX;

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();
}


function updateAirplaneVisuals(data) {
    const { airplane } = data;

    if (!airplane) return;

    document.getElementById('display-ground-distance').textContent = `${parseFloat(airplane.ground_distance).toFixed(2)} m`;
    document.getElementById('display-angulation').textContent = airplane.angulation;
    document.getElementById('display-flap-state').textContent = airplane.flap_state;
    const rpmVal = parseInt(airplane.rpm);
    document.getElementById('display-rpm').textContent = `${rpmVal.toLocaleString()} RPM`;
    
    updateRPMChart(rpmVal);

    const mappedGroundDistance = parseFloat(airplane.ground_distance);
    airplaneGroup.position.y = mappedGroundDistance;

    airplaneGroup.rotation.x = 0;
    airplaneGroup.rotation.z = 0;

    const tailHorizontalMesh = airplaneGroup.getObjectByName('tailHorizontal');
    const flapLeftMesh = airplaneGroup.getObjectByName('flapLeft');
    const flapRightMesh = airplaneGroup.getObjectByName('flapRight');

    if (tailHorizontalMesh) tailHorizontalMesh.rotation.x = 0;

    if (airplane.angulation === "LEFT_BANK") {
        airplaneGroup.rotation.z = Math.PI / 8;
    } else if (airplane.angulation === "RIGHT_BANK") {
        airplaneGroup.rotation.z = -Math.PI / 8;
    } else if (airplane.angulation === "UP") {
        airplaneGroup.rotation.x = -Math.PI / 10;
        if (tailHorizontalMesh) tailHorizontalMesh.rotation.x = -Math.PI / 8;
    } else if (airplane.angulation === "DOWN") {
        airplaneGroup.rotation.x = Math.PI / 10;
        if (tailHorizontalMesh) tailHorizontalMesh.rotation.x = Math.PI / 8;
    }

    let targetFlapRotation = (airplane.flap_state === "DOWN") ? Math.PI / 6 :
        (airplane.flap_state === "UP") ? -Math.PI / 12 : 0;

    if (flapLeftMesh) flapLeftMesh.rotation.x = targetFlapRotation;
    if (flapRightMesh) flapRightMesh.rotation.x = targetFlapRotation;

    currentRPM = rpmVal;

    applyHierarchicalFeedback(data, airplaneGroup);

    const jsonOutput = document.getElementById('json-output');
    if (jsonOutput) {
        jsonOutput.textContent = JSON.stringify(data, null, 2);
    }
}

const tempVector = new THREE.Vector3();

function updateLabelsPosition() {
    labelMeshes.forEach(item => {
        if (!labelsVisible) return; 
        
        tempVector.copy(item.mesh.position);

        item.mesh.updateWorldMatrix(true, false);
        tempVector.setFromMatrixPosition(item.mesh.matrixWorld);
        tempVector.project(camera);

        const x = (tempVector.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-tempVector.y * 0.5 + 0.5) * window.innerHeight;

        item.element.style.left = `${x}px`;
        item.element.style.top = `${y}px`;
    });
}


function animate() {
    requestAnimationFrame(animate);

    const rotationSpeed = currentRPM / 1000;
    const engineN1 = airplaneGroup.getObjectByName('engineN1');
    const engineN2 = airplaneGroup.getObjectByName('engineN2');

    const fanN1 = engineN1 ? engineN1.getObjectByName('fan') : null;
    const fanN2 = engineN2 ? engineN2.getObjectByName('fan') : null;

    if (fanN1) fanN1.rotation.z += rotationSpeed * 5;
    if (fanN2) fanN2.rotation.z += rotationSpeed * 5;

    updateLabelsPosition();

    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

function toggleLabelsVisibility() {
    labelsVisible = !labelsVisible; 
    
    document.querySelectorAll('.demarcation-label').forEach(label => {
        label.style.display = labelsVisible ? 'block' : 'none';
    });
}

window.addEventListener('keydown', (event) => {
    if (event.code === 'Space') {
        event.preventDefault(); 
        toggleLabelsVisibility();
    }
});

function fetchIAData() {
    const primaryDataFile = 'airplane.json'; 

    fetch(primaryDataFile)
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                return fetch('./front_end/airplane.txt')
                    .then(altResponse => {
                        if (!altResponse.ok) {
                            throw new Error('Falha ao carregar ambos os arquivos de dados (airplane.json e airplane.txt).');
                        }
                        return altResponse.text();
                    });
            }
        })
        .then(text => {
            let data;
            try {
                data = JSON.parse(text);
            } catch (e) {
                console.error("Erro ao analisar JSON. Verifique a formatação do arquivo.", e);
                return;
            }

            if (data && data.ariplane && !data.airplane) {
                data.airplane = data.ariplane;
            }
            
            if (data && data.airplane) {
                updateAirplaneVisuals(data);
            } else {
                console.warn("Dados carregados, mas a chave 'airplane' (ou 'ariplane') não foi encontrada na estrutura superior.");
            }
        })
        .catch(error => {
            console.error("Erro ao carregar dados. Verifique o caminho dos arquivos e permissões.", error);
        });
}

setInterval(fetchIAData, 3000);
fetchIAData();