<?
    include_once 'config.php'; // 資料庫連線資訊。

    $conn = mysqli_connect($db_host, $db_user, $db_pwd, $db_name);

    if ( ! $conn ) {
        exit;
    }

    $stmt = mysqli_prepare( $conn, "INSERT INTO WebHooks (token, team_id, team_domain, channel_id, channel_name, timestamp, user_id, user_name, text, trigger_word) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" );
    mysqli_stmt_bind_param( $stmt, 'ssssssssss', $token, $team_id, $team_domain, $channel_id, $channel_name, $timestamp, $user_id, $user_name, $text, $trigger_word );

    $token = $_REQUEST['token'];
    $team_id = $_REQUEST['team_id'];
    $team_domain = $_REQUEST['team_domain'];
    $channel_id = $_REQUEST['channel_id'];
    $channel_name = $_REQUEST['channel_name'];
    $timestamp = $_REQUEST['timestamp'];
    $user_id = $_REQUEST['user_id'];
    $user_name = $_REQUEST['user_name'];
    $text = $_REQUEST['text'];
    $trigger_word = $_REQUEST['trigger_word'];

    mysqli_stmt_execute( $stmt );
    mysqli_stmt_close( $stmt );
    mysqli_close( $conn );

    if ( $token != 'Token' || $user_name == 'slackbot' ) { // Outgoing WebHooks: 比對 Token 權杖，避開 slackbot 暱稱以免造成無窮回應。
        exit;
    }

    $payload = array(
        'channel' => '#random', // Channel 發言頻道。
        'username' => 'MyRobo' // Customize Name 機器人暱稱。
    );

    $showMenu = false;

    switch ( $trigger_word ) { // Trigger Word(s) 觸發關鍵字: 天氣,選單,好手氣
        case '天氣':
            $text = '今天相當晴朗炎熱。';
            break;
        case '選單':
            $showMenu = true;

            $menu = array(
                array(
                    'color' => '#36a64f',
                    'title' => "{$user_name} 這是您的選單:",
                    'title_link' => "https://myrobo.slack.com/team/{$user_name}",
                    'fields' => array(
                        array('title' => '1. 鬥陣特攻', 'value' => '千萬別玩', 'short' => false),
                        array('title' => '2. 俠盜獵車手', 'value' => '富貴險中求', 'short' => false),
                        array('title' => '3. 異塵餘生4', 'value' => '狗一樣的隊友', 'short' => false),
                        array('title' => '4. 超時空要塞Δ', 'value' => '禁絕邊境線', 'short' => false)
                    )
                )
            );

            break;
        case '好手氣':
            $text = '祝您中獎！';
            break;
    }

    if ( ! $showMenu ) {
        $payload['text'] = $user_name . ' ' . $text; // 一般回應訊息。
    } else {
        $payload['attachments'] = $menu; // 顯示 Message Attachments 當作選單。
    }

    $ctx = stream_context_create(array(
        'http' => array( // 雖然是 HTTPS 安全性連線，仍然沿用 http。
            'method'  => 'POST',
            'header'  => 'Content-Type: application/x-www-form-urlencoded', // POST 表單資料。
            'content' => http_build_query(array('payload' => json_encode( $payload )))
        )
    ));

    header('Content-Type: application/json'); // Outgoing WebHooks 的 Responding 回應並無作用(文件寫說可以直接做出回應)(X)，於是把 Incoming WebHooks 的回應 ok 塞回去。
    echo json_encode(
        array(
            'text' => file_get_contents( 'https://hooks.slack.com/services/team_id/services_id/url_id', false, $ctx ) // Incoming WebHooks: Webhook URL 傳送 JSON 裝載資料到 HTTPS 網址。
        )
    );
?>
