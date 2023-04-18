import requests

from utils.assertError import AssertError
import config
from api_test.channelManager.GetConnectionState import GetConnectionState
from interface.ApiInterfaceImpl import ApiImpl
from utils.time_utils import TimeUtils
from profile1.OnLocalVideoStats import OnLocalVideoStats
from profile1.OnRemoteVideoStats import OnRemoteVideoStats
from profile1.OnLocalAudioStats import OnLocalAudioStats
from profile1.OnRemoteAudioStats import OnRemoteAudioStats
from profile1.ProfileEnum import ProfileEnum
from numpy import mean
import time
import json
from utils.http_utils import HttpUtils
from utils.output_utils import OutputUtils
from distutils.util import strtobool
import random
from feature_test.QOS_auto_without_manul.commonData import global_cmmD
from feature_test.QOS_auto_without_manul.g2_web_ui.testcase.MOS_test.control import webclient

class ApiCommon:
    def __init__(self, user_list: list, enable_config=False):
        self.user_list = []
        self.time_cid = TimeUtils.get_time_format1(0)
        self.start_time = 0
        self.end_time = 0
        self.bw_drop_enable = False

        self.get_safe_mode_token_url = 'https://nrtc.netease.im/demo/getChecksum.action' \
                                       '?appkey=' + str(config.AppKey) + '&uid='
        for arg in user_list:
            OutputUtils.print(arg)
            self.user_list.append(ApiImpl(arg))
        self.init_demo_config(enable_config)

    def SetChannelProfile(self, profile: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetChannelProfile(profile))

    def SetH265(self, h265="1", nevc="0"):
        for i in self.user_list:
            i.SetH265(h265, nevc)

    def SetParameters(self, user: int, video_prefer_hw_encoder=True, video_prefer_hw_decoder=True,
                      auto_subscribe_audio=True, record_video_enabled=False, test_1v1=False, video_sendonpub_type=1,
                      auto_subscribe_video=False):
        if self.user_list[user].platform == config.ANDROID:
            ApiCommon.assert_error(
                self.user_list[user].AosSetParameters(video_prefer_hw_encoder=video_prefer_hw_encoder,
                                                      video_prefer_hw_decoder=video_prefer_hw_decoder,
                                                      auto_subscribe_audio=auto_subscribe_audio,
                                                      record_video_enabled=record_video_enabled,
                                                      test_1v1=test_1v1,
                                                      video_sendonpub_type=video_sendonpub_type,
                                                      auto_subscribe_video=auto_subscribe_video))
        elif self.user_list[user].platform == config.IOS:
            ApiCommon.assert_error(
                self.user_list[user].IosSetParameters(video_prefer_hw_encoder=video_prefer_hw_encoder,
                                                      video_prefer_hw_decoder=video_prefer_hw_decoder,
                                                      auto_subscribe_audio=auto_subscribe_audio,
                                                      record_video_enabled=record_video_enabled,
                                                      test_1v1=test_1v1,
                                                      video_sendonpub_type=video_sendonpub_type,
                                                      auto_subscribe_video=auto_subscribe_video))
        else:
            ApiCommon.assert_error(self.user_list[user].SetParameters(auto_subscribe_audio=auto_subscribe_audio,
                                                                      record_video_enabled=record_video_enabled,
                                                                      test_1v1=test_1v1,
                                                                      video_sendonpub_type=video_sendonpub_type,
                                                                      auto_subscribe_video=auto_subscribe_video))

    def SetPrivateParams(self, private_params: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetPrivateParams(private_params=private_params))

    def SetPubType(self, video_sendonpub_type=1):
        """
        kNERtcSendOnPubNone = 0, /**< 不主动发送数据流，被订阅后发送。 */
        kNERtcSendOnPubHigh = 1, /**< 主动发送大流。 */
        kNERtcSendOnPubLow = 1 << 1, /**< 主动发送小流。 */
        kNERtcSendOnPubAll = kNERtcSendOnPubLow | kNERtcSendOnPubHigh, /**< 主动发送大小流。 */
        """
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetParameters(video_sendonpub_type=video_sendonpub_type,
                                                       auto_start_local_audio=False,
                                                       auto_start_local_video=False))
                #ApiCommon.assert_error(i.SetSendOnPubType(video_sendonpub_type=video_sendonpub_type))
            elif i.platform == config.MAC:
                ApiCommon.assert_error(i.SetParameters(video_sendonpub_type=video_sendonpub_type))
            elif i.platform == config.IOS:
                ApiCommon.assert_error(i.IosSetParameters(video_sendonpub_type=video_sendonpub_type))
            else:
                ApiCommon.assert_error(i.AosSetParameters(video_sendonpub_type=video_sendonpub_type,
                                                          media_url=None))

    def AdjustRecordingSignalVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.AdjustRecordingSignalVolume(volume))

    def AdjustPlaybackSignalVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.AdjustPlaybackSignalVolume(volume))

    def AdjustUserPlaybackSignalVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.AdjustUserPlaybackSignalVolume(volume))

    def SetAudioMixingPlaybackVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetAudioMixingPlaybackVolume(volume))

    def GetAudioMixingPlaybackVolume(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.GetAudioMixingPlaybackVolume())

    def SetAudioMixingSendVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetAudioMixingSendVolume(volume))

    def GetAudioMixingSendVolume(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.GetAudioMixingSendVolume())

    def init_demo_config(self, enable_config):
        for i in self.user_list:
            if len(i.cpu) > 0 and enable_config:
                i.SetSuperResolution(value="0")
                i.SetH265(h265='0', nevc='0')

    def initialize(self,
                   video_prefer_hw_encoder=False,
                   video_prefer_hw_decoder=False,
                   app_key=None,
                   channel_name=None,
                   private_address=False):
        for i in self.user_list:
            # i.SetMediaUrl()
            if i.platform == config.WEB:
                continue
            i.Release()
            if i.platform == config.ANDROID:
                ApiCommon.assert_error(i.AosSetParameters(video_prefer_hw_encoder=video_prefer_hw_encoder,
                                                          video_prefer_hw_decoder=video_prefer_hw_decoder))
                result = i.initialize(log_level=3, app_key=app_key, private_address=private_address)
                ApiCommon.assert_error(result)
            elif i.platform == config.MAC:
                time.sleep(2)
                i.SetParameters()
                result = i.initialize(log_level=3,
                                      video_prefer_hw_encoder=video_prefer_hw_encoder,
                                      video_prefer_hw_decoder=video_prefer_hw_decoder,
                                      app_key=app_key,
                                      private_address=private_address)
                ApiCommon.assert_error(result)
            elif i.platform == config.IOS:
                time.sleep(5)
                i.IosSetParameters()
                result = i.initialize(log_level=3,
                                      app_key=app_key,
                                      video_prefer_hw_encoder=video_prefer_hw_encoder,
                                      video_prefer_hw_decoder=video_prefer_hw_decoder,
                                      private_address=private_address,)
                ApiCommon.assert_error(result)
            else:
                i.SetParameters()
                ApiCommon.assert_error(i.initialize(log_level=3,
                                                    init=True,
                                                    app_key=app_key,
                                                    private_address=private_address))
            # if private_address:
            #     i.SetPrivateAddress(False)
        # self.get_drop_bw_strategy()
    def initialize_exnternal_render(self,
                   user:int,
                   video_prefer_hw_encoder=False,
                   video_prefer_hw_decoder=False,
                   app_key=None,
                   private_address=False,
                   exnternal_render=False,
                   av_sync_is_main=False,
                   av_sync_uid=-1):
        i = self.user_list[user]
        # i.SetMediaUrl()
        if i.platform == config.WEB:
            return
        i.Release()
        if i.platform == config.ANDROID:
            ApiCommon.assert_error(i.AosSetParameters(video_prefer_hw_encoder=video_prefer_hw_encoder,
                                                      video_prefer_hw_decoder=video_prefer_hw_decoder))
            result = i.initialize(log_level=3, app_key=app_key, private_address=private_address,
                                  exnternal_render=exnternal_render,av_sync_is_main=av_sync_is_main,av_sync_uid=av_sync_uid)
            ApiCommon.assert_error(result)
        elif i.platform == config.MAC:
            time.sleep(2)
            i.SetParameters()
            result = i.initialize(log_level=3,
                                  video_prefer_hw_encoder=video_prefer_hw_encoder,
                                  video_prefer_hw_decoder=video_prefer_hw_decoder,
                                  app_key=app_key,
                                  private_address=private_address,
                                  exnternal_render=exnternal_render, av_sync_is_main=av_sync_is_main,
                                  av_sync_uid=av_sync_uid)

            ApiCommon.assert_error(result)
        elif i.platform == config.IOS:
            i.IosSetParameters()
            result = i.initialize(log_level=3,
                                  app_key=app_key,
                                  video_prefer_hw_encoder=video_prefer_hw_encoder,
                                  video_prefer_hw_decoder=video_prefer_hw_decoder,
                                  private_address=private_address,
                                  exnternal_render=exnternal_render, av_sync_is_main=av_sync_is_main,
                                  av_sync_uid=av_sync_uid)

            ApiCommon.assert_error(result)
        else:
            i.SetParameters()
            ApiCommon.assert_error(i.initialize(log_level=3,
                                                init=True,
                                                app_key=app_key,
                                                private_address=private_address,
                                                exnternal_render=exnternal_render, av_sync_is_main=av_sync_is_main,
                                                av_sync_uid=av_sync_uid)
                                   )

    def SetVideoConfig(self, maxProfile=2, cropMode=0,
                       frameRate=0, minFrameRate=0,
                       maxBitrate=0, minBitrate=0,
                       width=0, height=0,
                       degradationPreference=0,
                       frontCamera=True,
                       mirrorMode=0, colorFormat=0,
                       orientationMode=0):
        for i in self.user_list:
            # frameRate = self.convert(i, frameRate)
            result = i.SetVideoConfig(maxProfile=maxProfile, cropMode=cropMode, frameRate=frameRate,
                                      minFrameRate=minFrameRate, maxBitrate=maxBitrate, minBitrate=minBitrate,
                                      width=width, height=height,
                                      degradationPreference=degradationPreference,orientationMode=orientationMode,
                                      frontCamera=frontCamera, mirrorMode=mirrorMode,colorFormat=colorFormat)
            ApiCommon.assert_error(result)
            # if i.platform == config.WINDOWS or i.platform == config.MAC:

    def SubRoomSetVideoConfig(self, maxProfile=0, cropMode=0,
                              frameRate=0, minFrameRate=0,
                              maxBitrate=0, minBitrate=0,
                              width=0, height=0,
                              degradationPreference=0,
                              frontCamera=True,
                              mirrorMode=0, colorFormat=0,
                              orientationMode=0,
                              channelName=-1):
        for i in self.user_list:
            result = i.SetVideoConfig(maxProfile=maxProfile, cropMode=cropMode, frameRate=frameRate,
                                      minFrameRate=minFrameRate, maxBitrate=maxBitrate, minBitrate=minBitrate,
                                      width=width, height=height,
                                      degradationPreference=degradationPreference, orientationMode=orientationMode,
                                      frontCamera=frontCamera, mirrorMode=mirrorMode, colorFormat=colorFormat,
                                      channelName=channelName)
            ApiCommon.assert_error(result)

    def JoinChannle(self, channel_name: str, get_token=False):
        cid = 0
        channel_name = str(channel_name)
        self.start_time = TimeUtils.get_cur_time()
        OutputUtils.print("加入房间时间：" + self.start_time.strftime(TimeUtils.time_format1))
        for i in self.user_list:
            token = None
            if get_token:
                data1 = HttpUtils.post_by_from(self.get_safe_mode_token_url + i.info["userId"])
                ApiCommon.assert_result(200, data1["code"])
                token = data1["checksum"]

            if i.platform == config.WEB:
                OutputUtils.print("进入web自动化")
                webstart_param = {
                    "url": "https://webnrtc.netease.im/G2%20dev/4.6.20/v4.6.20/webrtc2.html",
                    "ip1": i.info["ip"],
                    "port1": i.info["port"],
                    "uid1": i.info["userId"],
                    "resolution_profile": global_cmmD.webresolution,
                    "frame_profile": global_cmmD.webframerate,
                    "address": global_cmmD.address,
                }
                # cname = str(time.time()).split(".")[0]  # 房间号
                cname = channel_name
                webclient.start_web_test(testid=cname, **webstart_param)
            elif i.platform == config.MAC:
                ApiCommon.assert_error(i.StartP2PView(channel_name, i.info["userId"]))
                ApiCommon.assert_error(i.JoinChannle(channel_name, i.info["userId"], token))
            elif i.platform != config.WINDOWS:
                ApiCommon.assert_error(i.JoinChannle(channel_name, i.info["userId"], token))
            else:
                ApiCommon.assert_error(i.StartP2PView(channel_name, i.info["userId"]))
            time.sleep(3)
            if i.platform != config.WEB:
                cid1 = GetConnectionState(i.info).get_success_status()
                if cid1 is not None:
                    cid = cid1
                OutputUtils.print(i.platform + " : 房间cid: " + str(cid))
        return cid

    def SetCameraCaptureConfig(self, captureHeight: int,
                       captureWidth: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetCameraCaptureConfig(captureHeight, captureWidth))


    def SetLocalRenderMode(self, scalingMode: int,mirrorMode=0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalRenderMode(scalingMode,mirrorMode))

    def SetRemoteRenderMode(self, scalingMode: int):
        for i in self.user_list:
            if i.platform != config.ANDROID:
                ApiCommon.assert_error(i.SetRemoteRenderMode(i.uid, scalingMode))

    def SwitchChannel(self, channel_name: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SwitchChannel(channel_name))

    def StartVideoPreview(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StartVideoPreview())

    def SetupLocalVideoCanvas(self, scalingMode: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetupLocalVideoCanvas(scalingMode))

    def HandlePreviewUI(self, openUI: bool):
        for i in self.user_list:
            if i.platform == config.IOS:
                ApiCommon.assert_error(i.handlePreviewUI(openUI))


    def StopVideoPreview(self):
        for i in self.user_list:
            i.StopVideoPreview()

    def SetLocalVideoMirrorMode(self, mirrorMode: int):
        for i in self.user_list:
            if i.platform != config.ANDROID and i.platform != config.IOS:
                ApiCommon.assert_error(i.SetLocalVideoMirrorMode(mirrorMode))

    def EnableLocalAudio(self, enabled: bool):
        for i in self.user_list:
            if i.platform == config.WEB:
                continue
            else:
                ApiCommon.assert_error(i.EnableLocalAudio(enabled))

    def EnableMediaPub(self, enable: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableMediaPub(enable))

    def SwitchCamera(self):
        for i in self.user_list:
            if i.platform != config.WINDOWS and i.platform != config.MAC:
                ApiCommon.assert_error(i.SwitchCamera())

    def SwitchCamera(self, position: int = 0):
        for i in self.user_list:
            if i.platform != config.WINDOWS and i.platform != config.MAC:
                ApiCommon.assert_error(i.SwitchCameraWithPosition(position))

    def EnableLocalVideo(self, enabled: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableLocalVideo(enabled))

    def MuteLocalVideoStream(self, mute: bool):
        for i in self.user_list:
            if i.platform == config.WEB:
                continue
            else:
                ApiCommon.assert_error(i.MuteLocalVideoStream(mute))

    def SubscribeRemoteVideoStream(self, subscribe: bool, streamType: int = 0):
        for i in self.user_list:
            uid = str(self.get_uid(i.info["userId"]))
            ApiCommon.assert_error(i.SubscribeRemoteVideoStream(uid, subscribe, streamType))

    def StartAudioDump(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StartAudioDump())

    def StartAudioDumpWithConfig(self, dumpType: int = 0):
        for i in self.user_list:
            ApiCommon.assert_error(i.StartAudioDumpWithType(dumpType))

    def StopAudioDump(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StopAudioDump())

    def SetClientRole(self, role: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetClientRole(role))

    def MuteLocalAudioStream(self, audioMuted: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.MuteLocalAudioStream(audioMuted))

    def StartAudioMixing(self, path: str = "http://mpge.5nd.com/2015/2015-11-26/69708/1.mp3", loopCount: int=1,
                         sendEnabled = True, playbackEnabled = True, sendVolume = 100, playbackVolume = 100,
                         startTime = 0,audioType = 0,progressInterval = 0):
        for i in self.user_list:
            if i.platform == config.WEB:
                continue
            else:
               	ApiCommon.assert_error(i.StartAudioMixing(path, loopCount, sendEnabled, playbackEnabled, sendVolume, playbackVolume, startTime, audioType, progressInterval))

    def PauseAudioMixing(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.PauseAudioMixing())

    def ResumeAudioMixing(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.ResumeAudioMixing())

    def StopAudioMixing(self):
        for i in self.user_list:
            if i.platform == config.WEB:
                continue
            else:
                ApiCommon.assert_error(i.StopAudioMixing())

    def GetAudioMixingPlaybackVolume(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.GetAudioMixingPlaybackVolume())

    def SetAudioMixingPlaybackVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetAudioMixingPlaybackVolume(volume))

    def SetAudioMixingSendVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetAudioMixingSendVolume(volume))

    def SubscribeRemoteAudioStream(self, subscribe: bool):
        for i in self.user_list:
            for j in range(len(self.user_list)):
                uid = self.user_list[j].info["userId"]
                if uid != i.info["userId"]:
                    ApiCommon.assert_error(i.SubscribeRemoteAudioStream(uid, subscribe))

    def SetAudioProfile(self, audioProfile: int, audioScene: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetAudioProfile(audioProfile, audioScene))

    def SetLocalVoiceEqualizationPreset(self, which: int, bandFrequency: int=0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalVoiceEqualizationPreset(which, bandFrequency))

    def SetLocalVoicePitch(self, pitch: float):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalVoicePitch(pitch))

    def SetLocalVoiceReverbPreset(self, which: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalVoiceReverbPreset(which))

    def SetVoiceBeautifierPreset(self, which: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetVoiceBeautifierPreset(which))

    def SetLocalVoiceChangerPreset(self, which: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalVoiceChangerPreset(which))

    def EnableEarback(self, enabled: bool, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableEarback(enabled, volume))

    def SetEarbackVolume(self, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetEarbackVolume(volume))

    def PlayEffect(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.PlayEffect(effect_id))

    def PauseEffect(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.PauseEffect(effect_id))

    def PauseAllEffects(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.PauseAllEffects())

    def ResumeAllEffects(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.ResumeAllEffects())

    def ResumeEffect(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.ResumeEffect(effect_id))

    def StopEffect(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.StopEffect(effect_id))

    def GetEffectSendVolume(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.GetEffectSendVolume(effect_id))

    def GetEffectPlaybackVolume(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.GetEffectPlaybackVolume(effect_id))

    def SetEffectSendVolume(self, effect_id: int, volume: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetEffectSendVolume(effect_id, volume))

    def SetEffectPlayBackVolume(self, effect_id: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetEffectPlaybackVolume(effect_id))

    def PlayOnlineAudioMixing(self, url: str, loop=1):
        for i in self.user_list:
            ApiCommon.assert_error(i.PlayOnlineAudioMixing(url, loop))

    def StopAllEffects(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StopAllEffects())

    def EnableLocalSubStreamAudio(self, enabled: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableLocalSubStreamAudio(enabled))

    def SubscribeRemoteSubStreamAudio(self, uid: int, subscribe: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubscribeRemoteSubStreamAudio(uid, subscribe))

    def MuteLocalSubStreamAudio(self, mute: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.MuteLocalSubStreamAudio(mute))

    def SetExternalSubStreamAudioSource(self, enabled: bool, sampleRate: int, channels: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetExternalSubStreamAudioSource(enabled, sampleRate, channels))

    def PushExternalSubStreamAudioFrame(self, audio_type: int, sampleRate: int, channels: int, bytes_per_sample: int = 16, samples_per_channel: int =480, path: str='', enable: bool = False):
        for i in self.user_list:
            ApiCommon.assert_error(i.PushExternalSubStreamAudioFrame(audio_type, sampleRate, channels, bytes_per_sample, samples_per_channel, path, enable))

    def SetExternalAudioRender(self, enable: bool, sampleRate: int, channels: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetExternalAudioRender(enable, sampleRate, channels))

    def PushExternalAudioFrame(self, audio_type: int, sampleRate: int, channels: int, bytes_per_sample: int, samples_per_channel: int,
                               path: str = "", enable: bool = False):
        for i in self.user_list:
            ApiCommon.assert_error(i.PushExternalAudioFrame(audio_type, sampleRate, channels, bytes_per_sample, samples_per_channel, path, enable))

    def SetExternalAudioSource(self, enable: bool, sampleRate: int, channels: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetExternalAudioSource(enable, sampleRate, channels))

    def SetExternalVideoSource(self, enable: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetExternalVideoSource(enable))

    def SetCaptureDevice(self, device: str, format: int, rotation: int):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetCaptureDevice(device, format, rotation))

    def PushExternalVideoFrame(self, path: str, format: int = 0, rotation: int = 0):
        for i in self.user_list:
            ApiCommon.assert_error(i.PushExternalVideoFrame(path, format, rotation))

    def StartScreenCapture(self, profile=1, bitrate=0, frameRate=5, prefer=0):
        # 仅限iOS
        for i in self.user_list:
            if i.platform == config.IOS:
                ApiCommon.assert_error(i.StartScreenCaptureByWindowId(
                    profile=profile,
                    bitrate=bitrate,
                    frameRate=frameRate,
                    prefer=prefer))

    def StartScreenCaptureByWindowId(self, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        # 开启屏幕共享，共享范围为指定窗口的指定区域，就是应用窗口共享，Mac和Windows
        for i in self.user_list:
            if i.platform == config.WINDOWS or i.platform == config.MAC:
                ApiCommon.assert_error(i.StartScreenCaptureByWindowId(
                    profile=profile,
                    bitrate=bitrate,
                    frameRate=frameRate,
                    width=width,
                    height=height,
                    prefer=prefer))

    def SubRoomStartScreenCaptureByWindowId(self, channelName: str):
        #开启屏幕共享，共享范围为指定窗口的指定区域，就是应用窗口共享，Mac和Windows
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SubRoomStartScreenCaptureByWindowId(
                    channelName=channelName))
                    # profile=profile,
                    # bitrate=bitrate,
                    # frameRate=frameRate,
                    # width=width,
                    # height=height,
                    # prefer=prefer))


    def SubRoomStartScreenCaptureByScreenRect(self, channelName: str, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        #开启屏幕共享，共享范围为指定屏幕的指定区域。该方法仅适用于 Windows 平台，桌面与屏幕共享
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SubRoomStartScreenCaptureByScreenRect(
                    channelName=channelName,
                    profile=profile,
                    bitrate=bitrate,
                    frameRate=frameRate,
                    width=width,
                    height=height,
                    prefer=prefer
                ))

    def StartScreenCaptureByScreenRect(self, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        # 开启屏幕共享，共享范围为指定屏幕的指定区域。该方法仅适用于 Windows 平台，桌面与屏幕共享
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.StartScreenCaptureByScreenRect(
                    profile=profile,
                    bitrate=bitrate,
                    frameRate=frameRate,
                    width=width,
                    height=height,
                    prefer=prefer
                ))

    def EnableDualStreamMode(self, enabled: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableDualStreamMode(enabled))

    def UpdateScreenCaptureRegion(self, x: int = 100, y: int = 200, width: int = 100, height: int = 200):
        # 更新屏幕共享区域，Windows和Mac
        for i in self.user_list:
            if i.platform == config.WINDOWS or i.platform == config.MAC:
                ApiCommon.assert_error(i.UpdateScreenCaptureRegion(
                    x=x,
                    y=y,
                    width=width,
                    height=height
                ))

    def SubRoomUpdateScreenCaptureRegion(self, channelName: str, x: int = 100, y: int = 100, width: int = 100, height: int = 200):
        #更新屏幕共享区域，Windows和Mac
        for i in self.user_list:
            if i.platform == config.WINDOWS or i.platform == config.MAC:
                ApiCommon.assert_error(i.SubRoomUpdateScreenCaptureRegion(
                    channelName=channelName,
                    x=x,
                    y=y,
                    width=width,
                    height=height
                ))

    def SetCaptureProfile(self, profile: int):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetCaptureProfile(profile))

    def StopScreenCapture(self):
        for i in self.user_list:
            if i.platform == config.WINDOWS or i.platform == config.MAC:
                ApiCommon.assert_error(i.StopScreenCapture())

    def SetMainDevice(self, profile: int):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetMainDevice(profile))

    def SetSubDevice(self, profile: int):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetSubDevice(profile))

    def SetSubProfile(self, profile: int):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.SetSubProfile(profile))

    def SetSuperResolution(self, value):
        for i in self.user_list:
            i.SetSuperResolution(value=value)
            # ApiCommon.assert_error(i.SetSuperResolution(value=value))

    def EnableSuperResolution(self, enable=True):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableSuperResolution(enable))

    def EnableAudioVolumeIndication(self, enable: bool, interval: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableAudioVolumeIndication(enable, interval))

    def SendSEI(self, seiMsg: str, length: int):
        for i in self.user_list:
            ApiCommon.assert_error(i.SendSEI(seiMsg, length))

    def StartLastmileProbeTest(self, probeUplink: bool = True, probeDownlink: bool = True,
                               expectedUplinkBitratebps: int = 200000,
                               expectedDownlinkBitratebps: int = 200000):
        for i in self.user_list:
            ApiCommon.assert_error(i.StartLastmileProbeTest(probeUplink, probeDownlink, expectedUplinkBitratebps,
                                                            expectedDownlinkBitratebps))

    def StopLastmileProbeTest(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StopLastmileProbeTest())

    def SendSEIStreamType(self, seiMsg: str, length: int, type: int=0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SendSEIStreamType(seiMsg, length, type))

    def SetLocalCanvasWatermarkConfigs(self, watermark: str = "normal", streamType: int = 0,
                                       textOn: bool = False, timeStampOn: bool = False, imageOn: bool = False,
                                       fontColor: str = "0xFF0000FF", fontSize: int = 10,
                                       offsetX: int = 0, offsetY: int = 0,
                                       wmColor: str = "0x88888888", wmHeight: int = 0,
                                       wmWidth: int = 0, imageUrl: str = "waters/water1.png",
                                       timestamp_fontColor: str = "0xFF0000FF", timestamp_fontSize=10,
                                       timestamp_offsetX: int = 0, timestamp_offsetY: int = 0,
                                       timestamp_wmColor: str = "0x88888888", timestamp_wmWidth: int = 0,
                                       timestamp_wmHeight: int = 0, imageWidth: int = 0,
                                       imageHeight: int = 0, imageOffsetX: int = 0,
                                       imageOffsetY: int = 0, fps: int = 0,
                                       loop: bool = True
                                       ):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetLocalCanvasWatermarkConfigs(watermark, streamType, textOn, timeStampOn, imageOn,
                                                                    fontColor, fontSize, offsetX, offsetY,
                                                                    wmColor, wmHeight, wmWidth, imageUrl,
                                                                    timestamp_fontColor, timestamp_fontSize,
                                                                    timestamp_offsetX, timestamp_offsetY,
                                                                    timestamp_wmColor, timestamp_wmWidth,
                                                                    timestamp_wmHeight, imageWidth,
                                                                    imageHeight, imageOffsetX,
                                                                    imageOffsetY, fps,
                                                                    loop
                                                                    ))

    def SetRemoteCanvasWatermarkConfigs(self, watermark: str = "normal", streamType: int = 0,
                                       textOn: bool = True, timeStampOn: bool = False, imageOn: bool = False,
                                       fontColor: str = "0xFF0000FF", fontSize: int = 10,
                                       offsetX: int = 0, offsetY: int = 0,
                                       wmColor: str = "0x88888888", wmHeight: int = 0,
                                       wmWidth: int = 0, imageUrl: str = "waters/water1.png",
                                       timestamp_fontColor: str = "0xFF0000FF", timestamp_fontSize=10,
                                       timestamp_offsetX: int = 0, timestamp_offsetY: int = 0,
                                       timestamp_wmColor: str = "0x88888888", timestamp_wmWidth: int = 0,
                                       timestamp_wmHeight: int = 0, imageWidth: int = 0,
                                       imageHeight: int = 0, imageOffsetX: int = 0,
                                       imageOffsetY: int = 0, fps: int = 0,
                                       loop: bool = True, uid: int = 0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetRemoteCanvasWatermarkConfigs(watermark, streamType, textOn, timeStampOn, imageOn,
                                                                    fontColor, fontSize, offsetX, offsetY,
                                                                    wmColor, wmHeight, wmWidth, imageUrl,
                                                                    timestamp_fontColor, timestamp_fontSize,
                                                                    timestamp_offsetX, timestamp_offsetY,
                                                                    timestamp_wmColor, timestamp_wmWidth,
                                                                    timestamp_wmHeight, imageWidth,
                                                                    imageHeight, imageOffsetX,
                                                                    imageOffsetY, fps,
                                                                    loop, uid))

    def LeaveChannel(self, is_arrest=False):
        for i in self.user_list:
            if i.platform == config.WEB:
                continue
            result = ApiCommon.log(i.LeaveChannel())
            time.sleep(2)
            if is_arrest:
                ApiCommon.assert_error(result)
            i.UploadSdkInfo()
            time.sleep(6)
            self.end_time = TimeUtils.get_cur_time()
            OutputUtils.print("离开房间时间：" + self.end_time.strftime(TimeUtils.time_format1))

    def EnableEncryption(self, enable: bool, mode = 0, key: str = "afh8465478777777777464654564s"):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableEncryption(enable,
                                                      mode,
                                                      key))

    def EnableVideoCorrection(self, enable: bool = False):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableVideoCorrection(enable=enable))

    def SetVideoCorrectionConfig(self, enableMirror: bool = True, width: int = 0, height: int = 0,
                                   left_top_x: int = 0, left_top_y: int = 0,
                                   right_top_x: int = 0, right_top_y: int = 0,
                                   left_bottom_x: int = 0, left_bottom_y: int = 0,
                                   right_bottom_x: int = 0, right_bottom_y: int = 0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetVideoCorrectionConfig(enableMirror, width, height, left_top_x, left_top_y,
                                                                right_top_x, right_top_y, left_bottom_x, left_bottom_y,
                                                                right_bottom_x, right_bottom_y))

    '''
     开启或关闭虚拟背景
    '''
    def EnableVirtualBackground(self, enable: bool = False, path: str = "", bg_sourcetype: int = 0,
                                color: str = "0xffffff"):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableVirtualBackground(enable, path, bg_sourcetype, color))

    '''多房间方法'''

    def CreateChannel(self, channelName: str):
        for i in self.user_list:
            #if i.platform != config.MAC:
            ApiCommon.assert_error(i.CreateChannel(channelName))

    def SubRoomRelease(self, channelName: str):
        for i in self.user_list:
            i.SubRoomLeaveChannel(channelName)
            i.SubRoomRelease(channelName)

    def SubRoomJoinChannel(self, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomJoinChannel(subChannelName, i.info["userId"]))

    def SubRoomLeaveChannel(self, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomLeaveChannel(subChannelName))

    def SubRoomSetClientRole(self, role: int, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetClientRole(role, subChannelName))

    def SubRoomGetConnectionState(self, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_exception(3, i.SubRoomGetConnectionState(subChannelName))

    def SubRoomSetStatsObserver(self, subChannelName: str):
        for i in self.user_list:
            i.SubRoomSetStatsObserver(subChannelName)

    def SubRoomSetChannelCallback(self, subChannelName: str):
        for i in self.user_list:
            if i.platform != config.WINDOWS and i.platform != config.MAC:
                ApiCommon.assert_error(i.SubRoomSetChannelCallback(subChannelName))

    def SubRoomMuteLocalAudioStream(self, mute: bool, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomMuteLocalAudioStream(mute, subChannelName))

    def SubRoomEnableLocalAudio(self, enable: bool, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomEnableLocalAudio(enable, subChannelName))

    def SubRoomMuteLocalVideoStream(self, mute: bool, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomMuteLocalVideoStream(mute, subChannelName))

    def SubRoomEnableLocalVideo(self, enable: bool, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomEnableLocalVideo(enable, subChannelName))

    def SubRoomSetupLocalVideoCanvas(self, scalMode: int, subChannelName: str):
        for i in self.user_list:
            if i.platform != config.ANDROID and i.platform != config.IOS:
                ApiCommon.assert_error(i.SubRoomSetupLocalVideoCanvas(scalMode,subChannelName))

    def SubRoomSetupRemoteVideoCanvas(self, subChannelName: str):
        for i in self.user_list:
            if i.platform != config.ANDROID and i.platform != config.IOS:
                ApiCommon.assert_error(i.SubRoomSetupRemoteVideoCanvas(i.info["userId"], subChannelName))

    def SubRoomSetupLocalSubStreamVideoCanvas(self, scalingMode: int, subChannelName: str):
        for i in self.user_list:
            if i.platform != config.ANDROID and i.platform != config.IOS:
                ApiCommon.assert_error(i.SubRoomSetupLocalSubStreamVideoCanvas(scalingMode, subChannelName))

    def SubRoomSetLocalRenderMode(self, scalingMode: int, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetLocalRenderMode(scalingMode, subChannelName))

    def SubRoomSetRemoteRenderMode(self, scalingMode: int, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetRemoteRenderMode(scalingMode, subChannelName))

    def SubRoomEnableDualStreamMode(self, enable: bool, subChannelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomEnableDualStreamMode(enable, subChannelName))

    def SubRoomSubscribeRemoteAudio(self, subscribe: bool, channelName: str):
        for i in self.user_list:
            uid = str(self.get_uid(i.info["userId"]))
            ApiCommon.assert_error(i.SubRoomSubscribeRemoteAudio(uid, subscribe, channelName))

    def SubRoomSubscribeRemoteVideo(self, subscribe: bool, streamType: int, channelName: str):
        for i in self.user_list:
            uid = str(self.get_uid(i.info["userId"]))
            ApiCommon.assert_error(i.SubRoomSubscribeRemoteVideo(uid, subscribe, streamType, channelName))

    def SubRoomTakeLocalSnapshot(self, streamType: int, channelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomTakeLocalSnapshot(streamType, channelName))

    def SubRoomSendSEIStreamType(self, seiMsg: str, length: int, type: int, channelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSendSEIStream(seiMsg, length, type, channelName))

    def SubRoomSendSEI(self, seiMsg: str, length: int, channelName: str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSendSEI(seiMsg, length, channelName))

    def SubRoomSetLocalCanvasWatermarkConfigs(self,channelName: str, watermark: str = "normal", streamType: int = 0,
                                       textOn: bool = False, timeStampOn: bool = False, imageOn: bool = False,
                                       fontColor: str = "0xFF0000FF", fontSize: int = 10,
                                       offsetX: int = 0, offsetY: int = 0,
                                       wmColor: str = "0x88888888", wmHeight: int = 0,
                                       wmWidth: int = 0, imageUrl: str = "waters/water1.png",
                                       timestamp_fontColor: str = "0xFF0000FF", timestamp_fontSize=10,
                                       timestamp_offsetX: int = 0, timestamp_offsetY: int = 0,
                                       timestamp_wmColor: str = "0x88888888", timestamp_wmWidth: int = 0,
                                       timestamp_wmHeight: int = 0, imageWidth: int = 0,
                                       imageHeight: int = 0, imageOffsetX: int = 0,
                                       imageOffsetY: int = 0, fps: int = 0,
                                       loop: bool = True):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetLocalCanvasWatermarkConfigs(channelName, watermark, streamType, textOn, timeStampOn, imageOn,
                                                                    fontColor, fontSize, offsetX, offsetY,
                                                                    wmColor, wmHeight, wmWidth, imageUrl,
                                                                    timestamp_fontColor, timestamp_fontSize,
                                                                    timestamp_offsetX, timestamp_offsetY,
                                                                    timestamp_wmColor, timestamp_wmWidth,
                                                                    timestamp_wmHeight, imageWidth,
                                                                    imageHeight, imageOffsetX,
                                                                    imageOffsetY, fps,
                                                                    loop
                                                                    ))

    def SubRoomSetRemoteCanvasWatermarkConfigs(self, channelName: str, watermark: str = "normal", streamType: int = 0,
                                       textOn: bool = True, timeStampOn: bool = False, imageOn: bool = False,
                                       fontColor: str = "0xFF0000FF", fontSize: int = 10,
                                       offsetX: int = 0, offsetY: int = 0,
                                       wmColor: str = "0x88888888", wmHeight: int = 0,
                                       wmWidth: int = 0, imageUrl: str = "waters/water1.png",
                                       timestamp_fontColor: str = "0xFF0000FF", timestamp_fontSize=10,
                                       timestamp_offsetX: int = 0, timestamp_offsetY: int = 0,
                                       timestamp_wmColor: str = "0x88888888", timestamp_wmWidth: int = 0,
                                       timestamp_wmHeight: int = 0, imageWidth: int = 0,
                                       imageHeight: int = 0, imageOffsetX: int = 0,
                                       imageOffsetY: int = 0, fps: int = 0,
                                       loop: bool = True, uid: int = 0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetRemoteCanvasWatermarkConfigs(channelName, watermark, streamType, textOn, timeStampOn, imageOn,
                                                                    fontColor, fontSize, offsetX, offsetY,
                                                                    wmColor, wmHeight, wmWidth, imageUrl,
                                                                    timestamp_fontColor, timestamp_fontSize,
                                                                    timestamp_offsetX, timestamp_offsetY,
                                                                    timestamp_wmColor, timestamp_wmWidth,
                                                                    timestamp_wmHeight, imageWidth,
                                                                    imageHeight, imageOffsetX,
                                                                    imageOffsetY, fps,
                                                                    loop, uid))

    def SubRoomSetCameraCaptureConfig(self, mCapturePreference: int, captureHeight: int, captureWidth: int, channelName:str):
        for i in self.user_list:
            ApiCommon.assert_error(i.SubRoomSetCameraCaptureConfig(channelName, mCapturePreference, captureHeight, captureWidth))

    def GetChannelName(self, channelName: str):
        for i in self.user_list:
            ApiCommon.assert_exception(channelName, i.GetChannelName(channelName))

    def assertResolution(self, height, width, maxProfile=0, cropMode=0, user=0):
        if maxProfile == 0:
            if cropMode == 0:
                self.assert_width_high(height, width, 120, 160, self.user_list[user])
            elif cropMode == 1:
                self.assert_width_high(height, width, 90, 160, self.user_list[user])
            elif cropMode == 2:
                self.assert_width_high(height, width, 120, 160, self.user_list[user])
            elif cropMode == 3:
                self.assert_width_high(height, width, 120, 120, self.user_list[user])
        elif maxProfile == 1:
            if cropMode == 0:
                self.assert_width_high(height, width, 240, 320, self.user_list[user])
            elif cropMode == 1:
                self.assert_width_high(height, width, 180, 320, self.user_list[user])
            elif cropMode == 2:
                self.assert_width_high(height, width, 240, 320, self.user_list[user])
            elif cropMode == 3:
                self.assert_width_high(height, width, 240, 240, self.user_list[user])
        elif maxProfile == 2:
            if cropMode == 0:
                self.assert_width_high(height, width, 480, 640, self.user_list[user])
            elif cropMode == 1:
                self.assert_width_high(height, width, 360, 640, self.user_list[user])
            elif cropMode == 2:
                self.assert_width_high(height, width, 480, 640, self.user_list[user])
            elif cropMode == 3:
                self.assert_width_high(height, width, 480, 480, self.user_list[user])
        elif maxProfile == 3:
            if cropMode == 0:
                self.assert_width_high(height, width, 720, 1280, self.user_list[user])
            elif cropMode == 1:
                self.assert_width_high(height, width, 720, 1280, self.user_list[user])
            elif cropMode == 2:
                self.assert_width_high(height, width, 720, 960, self.user_list[user])
            elif cropMode == 3:
                self.assert_width_high(height, width, 720, 720, self.user_list[user])
        elif maxProfile == 4:
            if cropMode == 0:
                self.assert_width_high(height, width, 1080, 1920, self.user_list[user])
            elif cropMode == 1:
                self.assert_width_high(height, width, 1080, 1920, self.user_list[user])
            elif cropMode == 2:
                self.assert_width_high(height, width, 1080, 1440, self.user_list[user])
            elif cropMode == 3:
                self.assert_width_high(height, width, 1080, 1080, self.user_list[user])

    def assert_width_high(self, h, w, h1, w1, user):
        if user.platform == config.IOS or user.platform == config.ANDROID:
            if h != w1 and w != h1:
                OutputUtils.print("预期宽高:" + str(w1) + "/" + str(h1))
                if self.bw_drop_enable:
                    if h > w1 or w > h1:
                        raise BaseException("降带宽策略开启后，期望实际分辨率比预期分辨率大")
                else:
                    raise BaseException("发送的height、 width预期不符, 实际Width" + str(w) + "， 实际Height" + str(h) + " 预期宽高:" + str(w1) + "/" + str(h1))
        else:
            if h != h1 and w != w1:
                OutputUtils.print("预期宽高:" + str(h1) + "/" + str(w1))
                if self.bw_drop_enable:
                    if h > h1 or w > w1:
                        raise BaseException("降带宽策略开启后，期望实际分辨率比预期分辨率大")
                else:
                    raise BaseException("发送的height、 width预期不符, 实际Width" + str(w) + "， 实际Height" + str(h) + " 预期宽高:" + str(w1) + "/" + str(h1))

    def assert_remote_width_high(self, h, w, h1, w1, user):
        if user.platform == config.IOS or user.platform == config.ANDROID:
            if h != h1 and w != w1:
                OutputUtils.print("预期width:" + str(w1) + "/" + str(h1))
                raise BaseException("发送的height、 width预期不符, 实际Width" + str(w) + "， 实际Height" + str(h) + " 预期宽高:" + str(w1) + "/" + str(h1))
        else:
            if h != h1 and w != w1:
                OutputUtils.print("预期width:" + str(w1) + "/" + str(h1))
                raise BaseException("发送的height、 width预期不符, 实际Width" + str(w) + "， 实际Height" + str(h) + " 预期宽高:" + str(w1) + "/" + str(h1))

    def assert_corp(self, corp, width, height, user):
        if corp == 3:
            if width != height:
                raise BaseException("裁剪比例不是1X1！")
        elif corp == 2:
            if user.platform == config.ANDROID or user.platform == config.IOS:
                if (width / height) < 0.74 or (width / height) > 0.76:
                    raise BaseException("裁剪比例不是4X3！")
            else:
                if (height / width) < 0.75 or (height / width) > 0.76:
                    raise BaseException("裁剪比例不是4X3！")
        elif corp == 1:
            if user.platform == config.ANDROID or user.platform == config.IOS:
                if (width / height) < 0.5 or (width / height) > 0.57:
                    raise BaseException("裁剪比例不是16X9！")
            else:
                if (height / width) < 0.5 or (height / width) > 0.57:
                    raise BaseException("裁剪比例不是16X9！")
        elif corp == 0:
            OutputUtils.print("不裁剪:" + str(width) + "/" + str(height))

    def get_resolution(self, user, task_cases_id, subroom="-1", num: int = 0, layer=1, uid=-1):
        local_video_stats = user.GetProfileData(task_cases_id, ProfileEnum.onLocalVideoStats, subroom, uid)

        if num > 0:
            local_video_stats = local_video_stats[-num:-1]
        local_video_width_list = []
        local_video_height_list = []
        local_video_sent_bit_rate_list = []
        local_drop_bw_list =[]
        for video in local_video_stats:
            video_data = json.loads(video['_source']['data'])
            layer_type = video_data["layer_type"]
            if isinstance(layer_type, str):
                layType = int(layer_type)
            else:
                layType = layer_type
            if layer == layType:
                if isinstance(video_data[OnLocalVideoStats.width], str):
                    local_video_width_list.append(int(video_data[OnLocalVideoStats.width]))
                else:
                    local_video_width_list.append(video_data[OnLocalVideoStats.width])
                if isinstance(video_data[OnLocalVideoStats.height], str):
                    local_video_height_list.append(int(video_data[OnLocalVideoStats.height]))
                else:
                    local_video_height_list.append(video_data[OnLocalVideoStats.height])
                if isinstance(video_data[OnLocalVideoStats.sent_bitrate], str):
                    local_video_sent_bit_rate_list.append(int(video_data[OnLocalVideoStats.sent_bitrate]))
                else:
                    local_video_sent_bit_rate_list.append(video_data[OnLocalVideoStats.sent_bitrate])
                if OnLocalVideoStats.drop_bw_strategy_enabled in video_data:
                    if isinstance(video_data[OnLocalVideoStats.drop_bw_strategy_enabled], bool):
                        local_drop_bw_list.append(video_data[OnLocalVideoStats.drop_bw_strategy_enabled])
                    else:
                        local_drop_bw_list.append(bool(strtobool(video_data[OnLocalVideoStats.drop_bw_strategy_enabled])))


        OutputUtils.print("layer" + str(layer) + " 高: " + str(local_video_height_list))
        OutputUtils.print("layer" + str(layer) + " 宽: " + str(local_video_width_list))
        OutputUtils.print("layer" + str(layer) + " 码率: " + str(local_video_sent_bit_rate_list))

        if len(local_video_height_list) > 0:
            height = mean(local_video_height_list)
        else:
            height = 0
        if len(local_video_width_list) > 0:
            width = mean(local_video_width_list)
        else:
            width = 0
        if len(local_video_sent_bit_rate_list) > 0:
            bitrate = mean(local_video_sent_bit_rate_list)
        else:
            bitrate = 0

        if len(local_drop_bw_list) > 0:
            OutputUtils.print("降带宽策略开启: " + str(local_drop_bw_list))
            if local_drop_bw_list[-1]:
                self.bw_drop_enable = True
            else:
                self.bw_drop_enable = False


        return height, width, bitrate

    def get_remote_resolution(self, user, task_cases_id, subroom="-1", num: int = 0, uid=-1, layer=1):
        remote_video_stats = user.GetProfileData(task_cases_id, ProfileEnum.onRemoteVideoStats, subroom, uid)

        if num > 0:
            remote_video_stats = remote_video_stats[-num:-1]

        remote_video_width_list = []
        remote_video_height_list = []
        remote_video_rcv_bit_rate_list = []
        for video in remote_video_stats:
            video_data = json.loads(video['_source']['data'])
            layer_type = video_data["layer_type"]
            if isinstance(layer_type, str):
                layType = int(layer_type)
            else:
                layType = layer_type
            if layer == layType:
                if isinstance(video_data[OnRemoteVideoStats.width], str):
                    remote_video_width_list.append(int(video_data[OnRemoteVideoStats.width]))
                else:
                    remote_video_width_list.append(video_data[OnRemoteVideoStats.width])
                if isinstance(video_data[OnRemoteVideoStats.height], str):
                    remote_video_height_list.append(int(video_data[OnRemoteVideoStats.height]))
                else:
                    remote_video_height_list.append(video_data[OnRemoteVideoStats.height])
                if isinstance(video_data[OnRemoteVideoStats.received_bitrate], str):
                    remote_video_rcv_bit_rate_list.append(int(video_data[OnRemoteVideoStats.received_bitrate]))
                else:
                    remote_video_rcv_bit_rate_list.append(video_data[OnRemoteVideoStats.received_bitrate])
        OutputUtils.print("layer" + str(layer) + " 高: " + str(remote_video_width_list))
        OutputUtils.print("layer" + str(layer) + " 宽: " + str(remote_video_height_list))
        OutputUtils.print("layer" + str(layer) + " 码率: " + str(remote_video_rcv_bit_rate_list))

        if len(remote_video_width_list) > 0:
            width = mean(remote_video_width_list)
        else:
            width = 0
        if len(remote_video_height_list) > 0:
            height = mean(remote_video_height_list)
        else:
            height = 0
        if len(remote_video_rcv_bit_rate_list) > 0:
            bitrate = mean(remote_video_rcv_bit_rate_list)
        else:
            bitrate = 0

        if user.platform == config.ANDROID or user.platform == config.IOS:
            return width, height, bitrate
        else:
            return height, width, bitrate

    def get_remote_video_info(self, user, task_cases_id, subroom="-1", num: int = 0, uid=-1):
        remote_video_stats = user.GetProfileData(task_cases_id, ProfileEnum.onRemoteVideoStats, subroom, uid)

        remote_video_width_list = list(map(lambda x: int(json.loads(x["_source"]["data"])[OnRemoteVideoStats.width]),
                                           remote_video_stats))

        remote_video_height_list = list(map(lambda x: int(json.loads(x["_source"]["data"])[OnRemoteVideoStats.height]),
                                            remote_video_stats))
        remote_video_received_bit_rate_list = list(map(lambda x: int(json.loads(x["_source"]["data"])[OnRemoteVideoStats.
                                                                 received_bitrate]), remote_video_stats))

        if len(remote_video_width_list) > 0:
            width = mean(remote_video_width_list)
        else:
            width = 0
        if len(remote_video_height_list) > 0:
            height = mean(remote_video_height_list)
        else:
            height = 0
        if len(remote_video_received_bit_rate_list) > 0:
            bitrate = mean(remote_video_received_bit_rate_list)
        else:
            bitrate = 0

        return height, width, bitrate

    def get_capture_video_info(self, user, task_cases_id, subroom="-1", uid=-1):
        cap_video_stats = user.GetProfileData(task_cases_id, ProfileEnum.onLocalVideoStats, subroom, uid)

        cap_video_width_list = list(map(lambda x: int(json.loads(x["_source"]["data"])[OnLocalVideoStats.capture_width]),
                                           cap_video_stats))

        cap_video_height_list = list(map(lambda x: int(json.loads(x["_source"]["data"])[OnLocalVideoStats.capture_height]),
                                            cap_video_stats))

        if len(cap_video_width_list) > 0:
            width = mean(cap_video_width_list)
        else:
            width = 0
        if len(cap_video_height_list) > 0:
            height = mean(cap_video_height_list)
        else:
            height = 0

        return height, width

    def get_remote_videoprofile(self, user, task_cases_id, subroom="-1", num: int = 0, layer=1,uid=-1):
        '''获取远端分辨率'''
        remote_video_stats = user.GetProfileData(task_cases_id, ProfileEnum.onRemoteVideoStats, subroom, uid)

        if num > 0:
            remote_video_stats = remote_video_stats[-num:-1]

        remote_video_width_list = []
        remote_video_height_list = []
        remote_video_sent_bit_rate_list = []
        for video in remote_video_stats:
            video_data = json.loads(video['_source']['data'])
            layer_type = video_data["layer_type"]
            if isinstance(layer_type, str):
                layType = int(layer_type)
            else:
                layType = layer_type
            if layer == layType:
                if isinstance(video_data[OnRemoteVideoStats.width], str):
                    remote_video_width_list.append(int(video_data[OnRemoteVideoStats.width]))
                else:
                    remote_video_width_list.append(video_data[OnRemoteVideoStats.width])
                if isinstance(video_data[OnRemoteVideoStats.height], str):
                    remote_video_height_list.append(int(video_data[OnRemoteVideoStats.height]))
                else:
                    remote_video_height_list.append(video_data[OnRemoteVideoStats.height])
                if isinstance(video_data[OnRemoteVideoStats.received_bitrate], str):
                    remote_video_sent_bit_rate_list.append(int(video_data[OnRemoteVideoStats.received_bitrate]))
                else:
                    remote_video_sent_bit_rate_list.append(video_data[OnRemoteVideoStats.received_bitrate])

        OutputUtils.print("layer" + str(layer) + " 高: " + str(remote_video_height_list))
        OutputUtils.print("layer" + str(layer) + " 宽: " + str(remote_video_width_list))
        OutputUtils.print("layer" + str(layer) + " 码率: " + str(remote_video_sent_bit_rate_list))

        if len(remote_video_width_list) > 0:
            width = mean(remote_video_width_list)
        else:
            width = 0
        if len(remote_video_height_list) > 0:
            height = mean(remote_video_height_list)
        else:
            height = 0
        if len(remote_video_sent_bit_rate_list) > 0:
            bitrate = mean(remote_video_sent_bit_rate_list)
        else:
            bitrate = 0

        if user.platform == config.ANDROID or user.platform == config.IOS:
            return height, width, bitrate
        else:
            return height, width, bitrate

    def get_remote_audio_info(self, user, task_cases_id, subroom="-1", uid=-1, layer=0):
        list_bit_rate = []
        list_volume = []
        list_uid = []
        remote_audio_stats = user.GetProfileData(task_cases_id, ProfileEnum.onRemoteAudioStats, subroom, uid)
        for audio in remote_audio_stats:
            s_data = json.loads(audio['_source']['data'])
            s_type = s_data['layer_type']

            '''
            音频主流数据
            '''
            if layer == 0:
                if s_type == "kNERtcAudioStreamTypeMain" or s_type == "0" or s_type == 0:
                    list_bit_rate.append(int(s_data[OnRemoteAudioStats.received_bitrate]))
                    list_volume.append(int(s_data[OnRemoteAudioStats.volume]))
                    list_uid.append(int(s_data[OnRemoteAudioStats.uid]))
            elif layer == 1:
                if s_type == "kNERtcAudioStreamTypeSub" or s_type == "1" or s_type == 1:
                    list_bit_rate.append(int(s_data[OnRemoteAudioStats.received_bitrate]))
                    list_volume.append(int(s_data[OnRemoteAudioStats.volume]))
                    list_uid.append(int(s_data[OnRemoteAudioStats.uid]))

        OutputUtils.print("layer " + str(layer) + " 接收到的码率: " + str(list_bit_rate))
        OutputUtils.print("layer " + str(layer) + " 接收到的音量: " + str(list_volume))
        OutputUtils.print("layer " + str(layer) + " 接收到的用户列表: " + str(list_uid))

        if len(list_bit_rate) > 0:
            rcv_bit_rate = mean(list_bit_rate)
        else:
            rcv_bit_rate = 0

        if len(list_volume) > 0:
            rev_volume = mean(list_volume)
        else:
            rev_volume = 0

        return rcv_bit_rate, rev_volume

    def get_local_audio_info(self, user, task_cases_id, subroom="-1", uid=-1, layer=0):
        list_bit_rate = []
        list_volume = []
        local_audio_stats = user.GetProfileData(task_cases_id, ProfileEnum.onLocalAudioStats, subroom, uid)
        for audio in local_audio_stats:
            s_data = json.loads(audio['_source']['data'])
            s_type = s_data['layer_type']

            '''
            音频主流数据
            '''
            if layer == 0:
                if s_type == "kNERtcAudioStreamTypeMain" or s_type == "0" or s_type == 0:
                    list_bit_rate.append(int(s_data[OnLocalAudioStats.sent_bitrate]))
                    list_volume.append(int(s_data[OnLocalAudioStats.volume]))
            elif layer == 1:
                if s_type == "kNERtcAudioStreamTypeSub" or s_type == "1" or s_type == 1:
                    list_bit_rate.append(int(s_data[OnLocalAudioStats.sent_bitrate]))
                    list_volume.append(int(s_data[OnLocalAudioStats.volume]))

        OutputUtils.print("layer " + str(layer) + " 发送的码率: " + str(list_bit_rate))
        OutputUtils.print("layer " + str(layer) + " 发送的音量: " + str(list_volume))

        if len(list_bit_rate) > 0:
            bit_rate = mean(list_bit_rate)
        else:
            bit_rate = 0

        if len(list_volume) > 0:
            sent_volume = mean(list_volume)
        else:
            sent_volume = 0

        return bit_rate, sent_volume




    def ClearProfileData(self, task_cases_id: int):
        '''清除数据'''
        for i in self.user_list:
            i.ClearProfileData(task_cases_id)

    def SubRoomClearProfile(self, channelName: str):
        '''iOS退出房间仍会上报，用于iOS清除定时上报，不清除数据'''
        for i in self.user_list:
            i.SubRoomClearProfile(channelName)

    def IsCameraZoomSupported(self, result: str):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_result_in(result, i.IsCameraZoomSupported())

    def IsCameraFocusSupported(self, result: str):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_exception(result, i.IsCameraFocusSupported())

    def IsCameraExposurePositionSupported(self, result: str):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_result_in(result, i.IsCameraExposurePositionSupported())

    def SetCameraFocusPosition(self, position_x: float, position_y: float):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_exception(0, i.SetCameraFocusPosition(position_x, position_y))

    def SetCameraExposurePosition(self, position_x: float, position_y: float):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_exception(0, i.SetCameraExposurePosition(position_x, position_y))

    def SetCameraZoomFactor(self, factor: float):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_exception(0, i.SetCameraZoomFactor(factor))

    def GetCameraMaxZoom(self):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                data = i.GetCameraMaxZoom()
                if float(data["result"]) <= 0:
                    raise BaseException("获取最大缩放倍数失败")

    def SetCameraTorchOn(self, on: bool):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                i.SetCameraTorchOn(on)

    def CheckPermission(self):
        for i in self.user_list:
            if i.platform == config.ANDROID or i.platform == config.IOS:
                ApiCommon.assert_error(i.CheckPermission())

    def SetPlayoutDeviceMute(self, muted: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetPlayoutDeviceMute(muted))

    def GetPlayoutDeviceMute(self, muted: bool):
        for i in self.user_list:
            if i.platform == config.ANDROID :
                ApiCommon.assert_exception(muted, i.GetPlayoutDeviceMute())
            elif i.platform == config.IOS:
                ApiCommon.assert_error(i.GetPlayoutDeviceMute())

    def SetRecordDeviceMute(self, muted: bool):
        for i in self.user_list:
            #if i.platform == config.ANDROID or i.platform == config.IOS:
            ApiCommon.assert_error(i.SetRecordDeviceMute(muted))

    def GetRecordDeviceMute(self, muted: bool):
        for i in self.user_list:
            if i.platform == config.ANDROID:
                ApiCommon.assert_exception(muted, i.GetRecordDeviceMute())
            elif i.platform == config.IOS:
                ApiCommon.assert_error(i.GetRecordDeviceMute())

    def SingleUserJoinChannle(self, channel_name: str, user=0):
        cid = 0
        channel_name = str(channel_name)
        self.start_time = TimeUtils.get_cur_time()
        OutputUtils.print("加入房间时间：" + self.start_time.strftime(TimeUtils.time_format1))
        i = self.user_list[user]
        if i.platform == config.MAC:
            ApiCommon.assert_error(i.StartP2PView(channel_name, i.info["userId"]))
            ApiCommon.assert_error(i.JoinChannle(channel_name, i.info["userId"]))
        elif i.platform != config.WINDOWS:
            ApiCommon.assert_error(i.JoinChannle(channel_name, i.info["userId"]))
        else:
            ApiCommon.assert_error(i.StartP2PView(channel_name, i.info["userId"]))
        cid1 = GetConnectionState(i.info).get_success_status()
        if cid1 is not None:
            cid = cid1

        OutputUtils.print("房间cid: " + str(cid))
        return cid

    def TakeLocalSnapshot(self, streamType: int):
        for i in self.user_list:
            if streamType == 0:
                # if i.platform == config.ANDROID or i.platform == config.WINDOWS:
                    ApiCommon.assert_error(i.TakeLocalSnapshot(streamType))
            elif streamType == 1:
                    ApiCommon.assert_error(
                        i.TakeLocalSnapshot(streamType))

    def InitPstn(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.InitPstn())

    def PstnRelease(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.PstnRelease())

    def DirectCallHangup(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.DirectCallHangup())



    def ClearProfile(self):
        for i in self.user_list:
            i.ClearProfile()

    '''
    根据不同的参数获取到截图文件的文件名
    文件生成规则：local/remote_ + channel_ + uid_ + streamtype_ + time 
    '''
    def GetSnapshotFile(self, user=0, streamType: int=0, videoType: int=0, channel: str="", time: str=""):
        currentUser = self.user_list[user]
        filename = ""
        if currentUser.platform == config.ANDROID or currentUser.platform == config.IOS:
            if videoType == 0:
                if channel == "":
                    prefix = "local_" + self.user_list[user].uid
                else:
                    prefix = "local_" + channel + "_" + self.user_list[user].uid

            else:
                if channel == "":
                    prefix = "remote_" + self.user_list[user].uid
                else:
                    prefix = "remote_" + channel + "_" + self.user_list[user].uid

            if streamType == 0:
                if currentUser.platform == config.ANDROID:
                    filename = prefix + "_" + "main_" + time + ".jpg"
                else:
                    filename = prefix + "_" + "main_" + time + ".png"
            else:
                if currentUser.platform == config.ANDROID:
                    filename = prefix + "_" + "sub_" + time + ".jpg"
                else:
                    filename = prefix + "_" + "sub_" + time + ".png"

        return filename

    def convert(self, user, framerate):
        if (user.platform == config.ANDROID):
            androidframerate = 0
            if framerate == 30:
                androidframerate = 0
            elif framerate == 7:
                androidframerate = 1
            elif framerate == 10:
                androidframerate = 2
            elif framerate == 15:
                androidframerate = 3
            elif framerate == 24:
                androidframerate = 4
            return androidframerate
        else:
            return framerate


    def get_uid(self, cur_id: str) -> int:
        for j in range(len(self.user_list)):
            uid = self.user_list[j].info["userId"]
            if uid != cur_id:
                return uid

    def get_respone(self, url: str):
        return HttpUtils.get(url)

    def remove_platform(self, platform):
        for i in self.user_list.copy():
            if i.platform == platform:
                self.user_list.remove(i)

    def SetCloudProxy(self, proxyType: int = 0):
        '''0关闭，1开启'''
        for i in self.user_list:
            ApiCommon.assert_error(i.SetCloudProxy(proxyType))

    def SetAudoSubscribeVideo(self, auto_subscribe_video: bool = False):
        for i in self.user_list:
            i.SetAudoSubscribeVideo(auto_subscribe_video)

    def SetAudoSubscribeData(self, auto_subscribe_data: bool = False):
        for i in self.user_list:
            i.SetAudoSubscribeData(auto_subscribe_data)

    def EnableLocalData(self, enabled: bool):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableLocalData(enabled))

    def get_drop_bw_strategy(self,):
        appkey_configname = "video_test_*359"
        currentappkey = config.AppKey
        getjson_url = "http://config-test.netease.im/multimedia-conf/cc/console/%s?%s" % (appkey_configname, currentappkey)
        r = requests.get(getjson_url)
        post_rescode = r.status_code
        post_resdata = r.text
        OutputUtils.print("get_rescode：" + str(post_rescode))
        para_dict = ""
        resdata_dict = json.loads(post_resdata)  # str 转 dict
        if self.user_list[0].platform == config.WINDOWS:
            para_dict = resdata_dict['data'][0]['config']['pc']['common']['video.profile.rtc']['engine.video.drop_bw_strategy_enable']
        elif self.user_list[0].platform == config.IOS:
            para_dict = resdata_dict['data'][0]['config']['ios']['common']['video.profile.rtc'][
                'engine.video.drop_bw_strategy_enable']
        elif self.user_list[0].platform == config.ANDROID:
            para_dict = resdata_dict['data'][0]['config']['aos']['common']['video.profile.rtc'][
                'engine.video.drop_bw_strategy_enable']
        elif self.user_list[0].platform == config.MAC:
            para_dict = resdata_dict['data'][0]['config']['macos']['common']['video.profile.rtc'][
                'engine.video.drop_bw_strategy_enable']
        if para_dict or para_dict == "True":
            self.bw_drop_enable = True
        else:
            self.bw_drop_enable = False

        OutputUtils.print("drop_bw_strategy：" + str(self.bw_drop_enable))

        return para_dict

    ''''
    开启美颜
    '''
    def StartBeauty(self):
        for i in self.user_list:
            if i.platform == config.WINDOWS:
                ApiCommon.assert_error(i.StartBeauty("bin\\data\\beauty\\nebeauty"))
            else:
                ApiCommon.assert_error(i.StartBeauty())
    '''
    关闭美颜
    '''
    def StopBeauty(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.StopBeauty())
    '''
    开启 / 暂停美颜
    '''
    def EnableBeauty(self, enable : bool = False):
        for i in self.user_list:
            ApiCommon.assert_error(i.EnableBeauty(enable))

    '''
    设置美颜类型和强度
    '''
    def SetBeautyEffect(self, beautytype:int = 0, level:float=0):
        for i in self.user_list:
            ApiCommon.assert_error(i.SetBeautyEffect(beautytype,level))

    '''
    导入美颜资源或模型
    '''
    def AddTempleteWithPath(self, path, name):
        for i in self.user_list:
            ApiCommon.assert_error(i.AddTempleteWithPath(path, name))

    '''
    添加滤镜效果
    '''
    def AddBeautyFilter(self, position):
        for i in self.user_list:
            ApiCommon.assert_error(i.AddBeautyFilter(position))

    '''
    取消滤镜效果
    '''
    def RemoveBeautyFilter(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.RemoveBeautyFilter())

    '''
    添加贴纸效果
    '''
    def AddBeautySticker(self, sticker, position):
        for i in self.user_list:
            ApiCommon.assert_error(i.AddBeautyFilter(sticker, position))

    '''
    取消贴纸效果
    '''
    def RemoveBeautySticker(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.RemoveBeautySticker())

    '''
    添加美妆效果
    '''
    def AddBeautyMakeup(self, sticker, position):
        for i in self.user_list:
            ApiCommon.assert_error(i.AddBeautyMakeup(sticker, position))

    '''
    取消美妆效果
    '''
    def RemoveBeautyMakeup(self):
        for i in self.user_list:
            ApiCommon.assert_error(i.RemoveBeautyMakeup())



    @staticmethod
    def assert_error(result: dict):
        OutputUtils.print(result)
        AssertError.assert_str("0", result["result"])

    @staticmethod
    def assert_exception(err_code: str, result: dict):
        OutputUtils.print(result)
        AssertError.assert_str(err_code, result["result"])

    @staticmethod
    def assert_result_in(err_code: str, result: dict):
        OutputUtils.print(result)
        AssertError.assert_str_in(err_code, result["result"])

    @staticmethod
    def assert_result(err_code: str, result: str):
        OutputUtils.print(result)
        AssertError.assert_str(err_code, result)

    @staticmethod
    def log(result: dict):
        OutputUtils.print(result)
        return result
