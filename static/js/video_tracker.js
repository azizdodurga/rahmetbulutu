// 1. YouTube API scriptini sayfaya ekle
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

// 2. API hazır olduğunda oynatıcıyı oluştur
function onYouTubeIframeAPIReady() {
  player = new YT.Player('youtube-player', {
    videoId: VIDEO_SETTINGS.videoId,
    playerVars: {
      'start': Math.floor(VIDEO_SETTINGS.startSeconds), // Kaldığı saniyeden başlat
      'rel': 0,
      'modestbranding': 1,
      'playsinline': 1
    },
    events: {
      'onStateChange': onPlayerStateChange
    }
  });
}

// 3. Durum değişikliğini izle (Duraklatınca kaydet)
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PAUSED || event.data == YT.PlayerState.ENDED) {
    saveProgress(player.getCurrentTime());
  }
}

// 4. Veritabanına saniyeyi gönder
function saveProgress(seconds) {
  const data = new URLSearchParams();
  data.append('video_id', VIDEO_SETTINGS.videoId);
  data.append('position', seconds);

  fetch(VIDEO_SETTINGS.saveUrl, {
    method: 'POST',
    headers: {
      'X-CSRFToken': VIDEO_SETTINGS.csrfToken,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: data
  })
    .then(response => response.json())
    .catch(error => console.error("Kaydetme hatası:", error));
}

// 5. Her 15 saniyede bir otomatik yedekleme yap (Opsiyonel)
setInterval(() => {
  if (player && player.getPlayerState() == YT.PlayerState.PLAYING) {
    saveProgress(player.getCurrentTime());
  }
}, 15000);

