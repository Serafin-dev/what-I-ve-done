using UnityEngine;
using UnityEngine.UI;
using Master.Models;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.SceneManagement;
using System.Collections;
using System;
using TMPro;

public class RoundManager : MonoBehaviour {
	public static RoundManager instance;

	public bool test;
	public AtrilApuestas _atrilApuestas;
	public List<GameObject> players;
	//public List<GameObject> player_indicators;
	public List<TextMeshProUGUI> player_textoNombre;
	public TextMeshProUGUI txtCategory;
	//public TMPro.TextMeshProUGUI txtPozo;
	public GameObject betting;
	public GameObject FinishingRound;
	public List<Image> playerFinish;
	public PozoOriginal clsPozo;

	//[HideInInspector]
	//public int turno;
	//[HideInInspector]

	[HideInInspector]
	public User_Game userTurn;
	private List<User_Game> usersInGame;
	private GameManager _gameManager;
	private GameSocketManager _GameSocketManager;
	private int pozo;

	private bool questionSceneLoaded = false;

	[Header("Referencias a todos los contadores")]
	public Contador[] contadoresLibros = new Contador[4];
	public Contador[] contadoresApuesta = new Contador[4];
	public Contador contadorPozo;

	[Header("Luces de turno")]
	public GameObject[] avatarPlayer = new GameObject[4];
	Color[] colorDestino = new Color[4];
	public Color colorDesactivado = Color.grey;
	public Material[] materialesPlayers = new Material[4];
	public float velCambioColor = .9f;

	public TMPro.TextMeshProUGUI textoDebug;

	public bool mostrandoNuevaRonda = true;
	public bool mostrandoFinRonda = false;
	public GameObject infoNuevaRonda;
	public GameObject infoFinRonda;
	public GameObject infoFinApuestas;

	public bool[] yaPusoMínima = new bool[4];
	public bool[] yaEmitióMínima = new bool[4];

	void Awake() {
		_gameManager = GameManager.instance;
		_GameSocketManager = GameSocketManager.instance;
		instance = this;

	}

	void Start() {
		//NewRound(); -> no, se llama cuando viene el evento.
		terminaronAnimacionesIniciales = false;
	}

	private void InitAll() {
		usersInGame = _gameManager._round.users.Values.ToList();
		usersInGame.Sort((a, b) => a.turn - b.turn);

		txtCategory.text = _gameManager._round.category;

		contadorPozo.valorReal = _gameManager._round.jackpot;

		int cantPlayers = _gameManager._round.users.Count;

		for (int i = 0; i < 4; i++) {
			Debug.Log("nombre player " + i + " es " + usersInGame[i].name);
		
			yaPusoMínima[i] = false;
			yaEmitióMínima[i] = false;
			usersInGame[i].bet = 0;
			
		}


		userTurn = usersInGame[0]; //empieza el 1ro


	}


	public bool esMiTurno() {
		return userTurn.userID == _GameSocketManager.user.userID;
	}

	void PlayerOnOff(int i, bool estáPresente, bool esSuTurno ) {
		avatarPlayer[i].SetActive(estáPresente);
		materialesPlayers[i].color = esSuTurno ? Color.white : colorDesactivado;
		if (!estáPresente) player_textoNombre[i].text = "";
		//Debug.Log("jugador" + i + " (" + player_textoNombre[i].text + ") activo: " + activo);
		//Debug.Break();
	}

	public string idPlayerSeFue = "";
	public void PlayerSeFue(string userId) {
        for (int i = 0; i < 4; i++) {
			Debug.Log("comparo con id " + usersInGame[i].userID + ": " + (usersInGame[i].userID == userId).ToString());
			if (usersInGame[i].userID == userId) {
				PlayerOnOff(i, false, false);
			}
        }
	}

	private void Update()
	{
		textoDebug.text = "bet " + userTurn.name + ": " + userTurn.bet;
		for (int i = 0; i < 4; i++) {
			//seteo a qué color va
			//full color si es su turno o si ya apostaron y está esperando respuestas
			bool mostrar = userTurn.turn == (i + 1);
			if (_gameManager.pauseBetRound) mostrar = true;
			if (mostrandoNuevaRonda) mostrar = false;
			colorDestino[i] = mostrar ? Color.white : colorDesactivado;

			//ir lentamente a ese color
			materialesPlayers[i].color = Color.Lerp(materialesPlayers[i].color, colorDestino[i], velCambioColor);
		}


		if (_gameManager.newRound)
			NewRound();

		if(!_gameManager.pauseBetRound)
		{
			if (!_gameManager.betRoundEnd)
			{
				//esto lo hace siempre 
				_atrilApuestas.HideAndShow(esMiTurno() && terminaronAnimacionesIniciales);
				verificarApuesta();
				
				if (_gameManager._round.pairing && 
					_gameManager.userIdPairing != null) {

					//cambio el turno y llamo a ProcesaNuevoTurno().
					Debug.Log("---sig turno (pairing!). Turno era " + userTurn.turn.ToString());
					userTurn = usersInGame.Where(x => x.userID == _gameManager.userIdPairing).FirstOrDefault();
					Debug.Log("---sig turno (pairing!). Turno ahora es " + userTurn.turn.ToString());

					ProcesaNuevoTurno();
				}
			}
			else
			{
				//LLEGÓ LA PREGUNTA

				//programo la carga de escena de pregunta para más tarde
				Invoke(nameof(CargaEscenaPregunta), 3.5f);
				infoFinApuestas.SetActive(true);
				_gameManager.betRoundEnd = false;
			}
		}

		if (_gameManager.cargarEscenaDuelo) {
			_gameManager.cargarEscenaDuelo = false;
			SceneManager.LoadScene("Duelo");
			Debug.Log("cargó la escena duelo");

		}

		if (idPlayerSeFue != "") {
			PlayerSeFue(idPlayerSeFue);
			idPlayerSeFue = "";
		}

		ActualizarTodosLosContadores(); //por ahora

	}

	void CargaEscenaPregunta() {
		infoFinApuestas.SetActive(false);
		if (!questionSceneLoaded && _gameManager._question != null) {
			_gameManager.primeraRonda = false; //muestra la banda de ganador cuando recargue
			StartCoroutine(LoadSceneAsync());
			questionSceneLoaded = true;
		}

		PlayerFinishAnswer();
	}


	private void PlayerFinishAnswer()
	{
		int index = 0;
		_gameManager._round.users.Values.ToList().ForEach(user =>
		{
			if(user.left)
			{
				playerFinish[index].color = Color.grey;
			}
			else if(user.endTurn)
			{
				playerFinish[index].color = Color.green;
			}
			else if(!user.endTurn)
			{
				playerFinish[index].color = Color.red;
			}

			index++;
		});
	}

	IEnumerator LoadSceneAsync()
	{
		var asyncOperation = SceneManager.LoadSceneAsync("5-Preguntas", LoadSceneMode.Additive);

		while (!asyncOperation.isDone)
		{
			yield return null;
		}

		_gameManager.pauseBetRound = true;
		betting.SetActive(false);
		FinishingRound.SetActive(true);
		SceneManager.SetActiveScene(SceneManager.GetSceneByName("5-Preguntas"));
	}

	public void EmitirMonto()
	{
		if (esMiTurno())
		{
			//User_Game userInfo = _gameManager._round.users.Values.Where(x => x.userID == userTurn.userID).FirstOrDefault();
			/*
			//SE EMITE LA APUESTA
			int valorRel = Mathf.CeilToInt(AtrilApuestas.instance.sliderApuesta.value);
			int valorAEmitir = valorRel; //relativo
			if (!yaEmitióMínima[userTurn.turn - 1]) {
				valorAEmitir += valorLuz;
				yaEmitióMínima[userTurn.turn - 1] = true;
				//esto es porque la apuesta mínima no va al server, tengo que agregarla acá
			}

			//siempre absoluto
			*/

			Bet apuesta = new Bet();
			apuesta.bet = userTurn.bet;
			apuesta.left = userTurn.left;
			apuesta.roomID = _gameManager._room.id;
			apuesta.userID = userTurn.userID;
			apuesta.pairing = _gameManager._round.pairing;
			_GameSocketManager.EmitBetFunction(apuesta);

			//userTurn.bet += valorRel;
			//userTurn.books -= valorRel; //porque ya descontó la apueta mínima la primera vez.
			//el problema es sólo con el server, el front ya descontó la mínima.

			_atrilApuestas.ActualizarAtril(_gameManager._round);
			Debug.Log("sig turno desde Emitir Monto");
			SiguienteTurno();
		}
	}

	public void verificarApuesta()
	{
		if (_gameManager.refreshBet)
		{
			_atrilApuestas.ActualizarAtril(_gameManager._round);
			Debug.Log("sig turno desde verificar apuesta");
			SiguienteTurno();
			_gameManager.refreshBet = false;
		}
	}

	
	public void SiguienteTurno() {
		//cambio el turno y llamo a ProcesaNuevoTurno().
        Debug.Log("---sig turno. Turno era " + userTurn.turn.ToString());
        int turno = userTurn.turn + 1;
		if (turno > usersInGame.Count) {
			_gameManager._round.pairing = true;
			return;
		}
		userTurn = usersInGame.Where(x => x.turn == turno).FirstOrDefault();

		//bool playExitAnimation = true;
		Debug.Log("---sig turno. Turno ahora es " + userTurn.turn.ToString());

        ProcesaNuevoTurno();

    }

    private void ProcesaNuevoTurno() {
		//se llama en SiguienteTurno y desde ComienzaRondaApuestas.

		int turno = userTurn.turn;
		Debug.Log("procesando turno nº " + turno);
        if (!_gameManager._round.pairing) {


            //userTurn = usersInGame[turno];
            //playExitAnimation = true;
            AtrilApuestas.instance.HabilitarBtnIgualar(turno > 1);
        } else if (_gameManager.userIdPairing != null) {
            string userId = _gameManager.userIdPairing;
            userTurn = usersInGame.Where(x => x.userID == userId).FirstOrDefault();
            _gameManager.userIdPairing = null;
            //playExitAnimation = false;
            AtrilApuestas.instance.HabilitarBtnIgualar(true);
        }

		//si no le sacó el mínimo, le saca
		if (!yaPusoMínima[turno - 1]) {
			usersInGame[turno - 1].bet += valorLuz;  //--> ya trae del server ese valor en bet
			usersInGame[turno - 1].books -= valorLuz;
			yaPusoMínima[turno - 1] = true;
			Debug.Log($"turno {turno} hace apuesta automática de {valorLuz}");
			
			AtrilApuestas.instance.ActualizarBotonesAtril(); //responde a la nueva apuesta automática
		}


	}

	public int valorLuz = 50;
	public bool terminaronAnimacionesIniciales = false;

    public void NewRound()
	{
		Debug.Log("Se crea una nueva ronda");

		_gameManager.newRound = false;


		//todavía no se puede jugar, todavía hay que descontar la mínima ni iluminar a ningún jugador
		//todo eso se controla con la siguiente variable:
		terminaronAnimacionesIniciales = false;


		betting.SetActive(true);
		FinishingRound.SetActive(false);

		InitAll();

		ActualizarTodosLosContadores();

		_atrilApuestas.InitAtril(_gameManager._round);
		_atrilApuestas.ActualizarAtril(_gameManager._round);
		questionSceneLoaded = false;

		AtrilApuestas.instance.Ocultar();
		if (_gameManager.primeraRonda) {
			infoNuevaRonda.SetActive(true);
			mostrandoNuevaRonda = true;
			Invoke("FinAnimaciónNuevaRonda", 3f);
		} else {
			IniciarBandaFinRonda(_gameManager.ultimoUsuarioGanador, _gameManager.ultimaRtaCorrecta);
		}

	}

	void FinAnimaciónNuevaRonda() {
		infoNuevaRonda.SetActive(false);
		mostrandoNuevaRonda = false;
		ComienzaRondaApuestas();
	}

	public void IniciarBandaFinRonda(string nombreGanador, string rtaCorrecta) {
		Debug.Log("inicia banda fin ronda");

		mostrandoNuevaRonda = false;
		infoNuevaRonda.SetActive(mostrandoNuevaRonda);
		

		mostrandoFinRonda = true;
		infoFinRonda.SetActive(mostrandoFinRonda);


		infoFinRonda.transform.GetChild(1).GetComponent<TextMeshProUGUI>().text =
			(nombreGanador != null && nombreGanador != "")
			? "ganó " + nombreGanador
			: "no hay ganador";

		infoFinRonda.transform.GetChild(2).GetComponent<TextMeshProUGUI>().text
			= "la respuesta correcta era \r\n" + rtaCorrecta;

		Invoke("CambiaUnaBandaPorOtra", 5f);
	}

	void CambiaUnaBandaPorOtra() {
		mostrandoFinRonda = false;
		infoFinRonda.SetActive(mostrandoFinRonda);

		mostrandoNuevaRonda = true;
		infoNuevaRonda.SetActive(mostrandoNuevaRonda);
		infoNuevaRonda.GetComponent<Animator>().speed = 1f;

		Invoke("FinAnimaciónNuevaRonda", 3f);
	}

	[ContextMenu("prueba duelo")]
	void ComenzarDuelo() {
		Debug.Log("antes de cargar la escena duelo");
		UnityEngine.SceneManagement.SceneManager.LoadScene(7);
		Debug.Log("cargó la escena duelo");
	}

	void ComienzaRondaApuestas() {
		terminaronAnimacionesIniciales = true; //terminaron TODAS las animaciones, ya se puede jugar
		ProcesaNuevoTurno();
	}

	public void ActualizarTodosLosContadores() {
		pozo = 0;
        for (int i = 0; i < 4; i++) {

			player_textoNombre[i].text = usersInGame[i].name;
			contadoresLibros[i].valorReal = usersInGame[i].books;
			contadoresApuesta[i].valorReal = usersInGame[i].bet;
			pozo += usersInGame[i].bet;
			PlayerOnOff(i, !usersInGame[i].left, userTurn.userID == usersInGame[i].userID);
		}

		contadorPozo.valorReal = pozo;

	}

	public void ActualizaEstadosBotones() { 
		
	}
}