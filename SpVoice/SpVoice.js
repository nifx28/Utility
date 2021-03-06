var SVSFPurgeBeforeSpeak = 2; // 語音參數。 https://msdn.microsoft.com/en-us/library/ms720892(v=vs.85).aspx
var SpVoice = WScript.CreateObject("SAPI.SpVoice"); // Microsoft Speech API (SAPI) 5.3
var SpFileStream = WScript.CreateObject("SAPI.SpFileStream"); // 檔案串流。
//GetAudioOutputs(); // 顯示所有音效裝置。
//GetVoices(); // 顯示所有語音助理。
SpVoice.AudioOutput = SpVoice.GetAudioOutputs().Item(1); // VoiceMeeter Input 虛擬麥克風。
SpVoice.Voice = SpVoice.GetVoices().Item(0); // 語音助理：0 台灣女性 1 美國男性 2 美國女性 3 日本女性 4 英國女性。
SpVoice.Rate = 1; // 講話速率 -10 ~ 10。
SpVoice.Volume = 100; // 音量 0 ~ 100。
SpVoice.Speak("此節目由畫面上顯示的贊助商提供。", SVSFPurgeBeforeSpeak);
SpVoice.Speak("This program was brought to you by the sponsors here displayed.", SVSFPurgeBeforeSpeak);
/*
SpVoice.Voice = SpVoice.GetVoices().Item(3);
SpVoice.Speak("この番組は、ご覧のスポンサーの提供でお送りします。", SVSFPurgeBeforeSpeak);
SpVoice.Voice = SpVoice.GetVoices().Item(1);
SpVoice.Speak("This program was brought to you by the sponsors here displayed.", SVSFPurgeBeforeSpeak);
SpVoice.Voice = SpVoice.GetVoices().Item(2);
SpVoice.Speak("This program was brought to you by the sponsors here displayed.", SVSFPurgeBeforeSpeak);
SpVoice.Voice = SpVoice.GetVoices().Item(3);
SpVoice.Speak("This program was brought to you by the sponsors here displayed.", SVSFPurgeBeforeSpeak);
SpVoice.Voice = SpVoice.GetVoices().Item(4);
SpVoice.Speak("This program was brought to you by the sponsors here displayed.", SVSFPurgeBeforeSpeak);
*/
/*
SpFileStream.Open("C:\\path\\to\\sound.wav");
SpVoice.SpeakStream(SpFileStream); // 播放外部音訊檔案。
*/
/*
0: [ 喇叭 (2- High Definition Audio 裝置) ]
1: [ VoiceMeeter Input (VB-Audio VoiceMeeter VAIO) ]
*/
function GetAudioOutputs() { // 顯示所有音效裝置。
    var result = "", outputs = SpVoice.GetAudioOutputs(), len = outputs.Count;

    for (var i = 0; i < len; ++i) {
        result += i + ": [ " + outputs.Item(i).GetDescription() + " ]\n";
    }

    WScript.Echo(result);
}
/*
0: [ Microsoft Hanhan Desktop - Chinese (Taiwan) ]
1: [ Microsoft David Desktop - English (United States) ]
2: [ Microsoft Zira Desktop - English (United States) ]
3: [ Microsoft Haruka Desktop - Japanese ]
4: [ Microsoft Hazel Desktop - English (Great Britain) ]
*/
function GetVoices() { // 顯示所有語音助理。
    var result = "", voices = SpVoice.GetVoices(), len = voices.Count;

    for (var i = 0; i < len; ++i) {
        result += i + ": [ " + voices.Item(i).GetDescription() + " ]\n";
    }

    WScript.Echo(result);
}
