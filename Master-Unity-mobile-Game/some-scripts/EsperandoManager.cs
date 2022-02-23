using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using Master.Models;

public class EsperandoManager : MonoBehaviour {

	public GameObject parentPanel;
	public GameObject esperandoPrefab;
    private GameObject esperandoClone;
	private clsUtilidades _clsUtil;
	public int playersColoreados;
    public bool test;
    private int cantidadUsuarios;
    private Image[] imgUsers;
    private Text[] txtNameUsers;
    private GameManager _gameManager;

    //Botones
    public Button botonBuscarPartida;
    private Button cancelar;


    [Header("Luces de turno")]
    Color[] colorDestino = new Color[4];
    public Color colorDesactivado = Color.grey;
    public Material[] materialesPlayers = new Material[4];
    public float velCambioColor = .9f;
    
    void Start () {
        
        //Doy funcionalidad a los botones
        

        _gameManager = GameManager.Instance;
        _clsUtil = gameObject.AddComponent<clsUtilidades>();

        botonBuscarPartida.onClick.AddListener(run);


    }

    public void BuscarRoom() {
        botonBuscarPartida.onClick.AddListener(run);
    }


    [ContextMenu("prueba salir")]
    public void Desconectar() {
        GameSocketManager.Instance.OnApplicationQuit();
    }

	private void instanciarModuloCompleto(){
        GameObject esperandoInstance = _clsUtil.instanciarUIObjects(esperandoPrefab, parentPanel, new Vector2(0, 0), new Vector2(1f, 1f));
        cancelar = GameObject.Find("/Canvas/MenuPanel/EsperandoPartidaPanel(Clone)/obj_boton_cancelar").GetComponent<Button>();
        cancelar.onClick.AddListener(cancelarEspera);

        GameObject user;
        cantidadUsuarios = esperandoInstance.transform.Find("objPanelesPersonaje").childCount;
        imgUsers = new Image[cantidadUsuarios];
        txtNameUsers = new Text[cantidadUsuarios];

        for(int i=0; i < cantidadUsuarios; i++){
            user = esperandoInstance.transform.Find("objPanelesPersonaje/objRecuadro" + (i+1)).gameObject;

            imgUsers[i] = user.transform.Find("imgFondo").GetComponent<Image>();
            txtNameUsers[i] = user.transform.Find("txtNombre").GetComponent<Text>();
        }
    }
    
	void Update () {
		if(_gameManager._room != null){
            playersColoreados = _gameManager._room.inside;

            //coloreo y dps las igualo
            this.ColorearUsersEsperando (_gameManager._room.users);
            if(_gameManager._room.inside == _gameManager._room.max && _gameManager._round != null){
                
                _gameManager.SiguienteEscena();
                
            }
            /*
            if (_gameManager._room.inside == _gameManager._room.max && _gameManager._round == null) {
                _gameManager._round = new Round();
                _gameManager._room.gameEnd = false;
                _gameManager.betRoundEnd = false;
                _gameManager.pauseBetRound = false;
                _gameManager.newRound = true;

            }*/
        }
	}


	public void ColorearUsersEsperando (User_Game[] Users){
        for(int i=0; i < cantidadUsuarios; i++){ 
            //PERSONAJES FUERA
            if(i < playersColoreados)
            {
                //PERSONAJES ADENTRO
                imgUsers[i].color = new Color(1f, 1f, 1f, 1f);
                txtNameUsers[i].text = Users[i].name;
            }
            else
            {
                //PERSONAJES FUERA
                imgUsers[i].color = new Color(0.35f, 0.35f, 0.35f, 1f);
                txtNameUsers[i].text = "";
            }
        }
    }
        
    private void run()
    {
        GameObject.Instantiate(GameSocketManager.Instance);
        instanciarModuloCompleto();
    }
    
    //Cancela la espera de buscar jugadores
    private void cancelarEspera()
    {
        esperandoClone = GameObject.Find("/Canvas/MenuPanel/EsperandoPartidaPanel(Clone)");
        Destroy(esperandoClone);
    }
    

        
}
