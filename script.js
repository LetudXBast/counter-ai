function compterLettres() {
  const texte = document.getElementById('texteInput').value;
  fetch('https://letter-counter-api.onrender.com/api/count', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texte: texte })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('resultat').textContent =
      `Ton texte contient ${data.nb_lettres} lettres.`;
  })
  .catch(error => {
    console.error('Erreur :', error);
    document.getElementById('resultat').textContent =
      'Erreur pendant la communication avec le serveur.';
  });
}

function resumerAvecMistral() {
  const paragraphe = document.getElementById('texteMistral').value;
  const loading = document.getElementById('loadingMistral');
  const resultat = document.getElementById('resumeMistral');

  resultat.textContent = '';
  loading.style.display = 'block';
  loading.textContent = 'Résumé en cours...';

  fetch('https://letter-counter-api.onrender.com/api/llm-summary', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texte: paragraphe })
  })
  .then(response => response.json())
  .then(data => {
    loading.style.display = 'none';
    if (data.resume) {
      resultat.textContent = data.resume;
    } else {
      resultat.textContent = 'Aucun résumé trouvé.';
    }
  })
  .catch(error => {
    loading.style.display = 'none';
    resultat.textContent = 'Erreur pendant le résumé.';
    console.error('Erreur :', error);
  });
}

