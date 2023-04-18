import os
from interface import ApiInterface
from utils.socket_client import SocketClient
import json
import config
from profile1.ProfileEnum import ProfileEnum
from utils.http_utils import HttpUtils
from utils.output_utils import OutputUtils
from utils.time_utils import TimeUtils


class ApiImpl(ApiInterface.Interface):

    def __init__(self, info: dict):
        self.ip = info["ip"]
        self.port = info["port"]
        self.platform = info["platform"]
        self.info = info
        self.cpu = info["cpu"]
        self.uid = info["userId"]

    @staticmethod
    def getdata():
        return {"type": "command", "module": "client"}

    @staticmethod
    def getAppKey():
        return config.AppKey

    # 自定义
    '''
    Mac PC 启动Demo UI加入房间
    '''

    def StartP2PView(self, cid=234234, uid=234234):
        self.checkPlatform(config.MAC, config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "StartP2PView"
        data["cid"] = cid
        data["uid"] = uid
        return self.resultdata(data)

    def StartChannelView(self, channlName=234234, uid=234234):
        self.checkPlatform(config.MAC, config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "StartChannelView"
        data["channlName"] = channlName
        data["uid"] = uid
        return self.resultdata(data)

    '''使用ui 设置分辨率，早期版本使用，最新版本不需要调用'''

    def SetCaptureProfile(self, profile: int):
        """
        profile1: 0   640*480
        profile1: 1   1280*720
        profile1: 2   1920*1080
        profile1: 3   自定义
        """
        self.checkPlatform(config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "SetCaptureProfile"
        data["profile"] = profile
        return self.resultdata(data)

    '''
    调用 SetStatsObserver，注册统计信息观测器
    开启统计数据上报
    '''

    def SetProfile(self, switch=True):
        data = ApiImpl.getdata()
        data["method"] = "SetProfile"
        data["switch"] = switch
        return self.resultdata(data)

    def SetCallbackEx(self, switch=True):
        data = ApiImpl.getdata()
        data["method"] = "SetCallbackEx"
        data["switch"] = switch
        return self.resultdata(data)

    '''
    注册语音观测器对象。
    该方法用于设置音频采集和播放PCM回调，可用于声音处理等操作。当需要引擎给出 onAudioFrameDidRecord 或 onAudioFrameWillPlayback 回调时，需要使用该方法注册回调。
    '''

    def SetAudioFrameObserver(self, switch=True, uid=0,
                              curtime=TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioFrameObserver"
        data["timestamp"] = curtime
        if self.platform == config.LINUX:
            data["uid"] = str(uid)
        else:
            data["uid"] = uid
        data["switch"] = switch
        return self.resultdata(data)

    def SetMediaUrl(self, url="10.219.34.5:7000"):
        if self.platform == config.IOS:
            data = ApiImpl.getdata()
            data["method"] = "SetMediaUrl"
            data["media_url"] = url
            return self.resultdata(data)
        data1 = {"turn_server": url}
        result = None
        if self.platform == config.WINDOWS:
            result = HttpUtils.post(config.WINDOWS_NODE + "/set_json_config", data1=data1)
        elif self.platform == config.MAC:
            result = HttpUtils.post(config.MAC_NODE + "/set_json_config", data1=data1)
        if result is not None:
            if int(result["code"]) != 0:
                raise BaseException("设置media_url失败")

    def SetQuicUrl(self, url: str):
        self.checkPlatform(config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "SetQuicUrl"
        data["quic_url"] = url
        return self.resultdata(data)

    '''
    回调数据上报地址设置
    task_cases_id 一般用房间cname，查询条件之一
    url 上报服务端的http地址
    uid 是否指定上报数据的uid , 不指定默认为-1， 当用例里面有两个及两个以上设备上报数据的时候，必须指定uid, 否则2个设备的数据会串
    open 默认开始上报，open=False的时候关闭上报
    '''

    def SetReportUrl(self, task_cases_id: int, url=config.MAIN_NODE + "/es/addReportData", uid=-1, open=True):
        data = ApiImpl.getdata()
        data["method"] = "SetReportUrl"
        data["url"] = url
        data["task_cases_id"] = task_cases_id
        if self.platform == config.LINUX:
            data["uid"] = str(uid)
        else:
            data["uid"] = uid
        data["open"] = open
        return self.resultdata(data)

    '''
    ios 端清除注册的observer
    '''

    def ClearProfile(self):
        if self.platform == config.IOS:
            data = ApiImpl.getdata()
            data["method"] = "ClearProfile"
            return self.resultdata(data)

    '''
    双摄设置使用-开启子摄像头
    '''

    def SetStartSubVideo(self):
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetStartSubVideo"
            return self.resultdata(data)

    '''
    双摄设置使用-设置主摄像头
    '''

    def SetMainDevice(self, profile: int):
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetMainDevice"
            data["profile"] = profile
            return self.resultdata(data)
        return None

    '''
    双摄设置使用-设置子摄像头
    '''

    def SetSubDevice(self, profile: int):
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetSubDevice"
            data["profile"] = profile
            return self.resultdata(data)

    '''
    双摄设置使用-设置子摄像头分辨率
    '''

    def SetSubProfile(self, profile: int):
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetSubProfile"
            data["profile"] = profile
            return self.resultdata(data)

    def DeleteProfile(self):
        data = ApiImpl.getdata()
        data["method"] = "DeleteProfile"
        return self.resultdata(data)

    '''
    获取cid
    '''

    def GetCurChannelId(self):
        # self.checkPlatform(config.WINDOWS, config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "GetCurChannelId"
        return self.resultdata(data)

    def GetRecvWidthHeight(self):
        data = ApiImpl.getdata()
        data["method"] = "GetRecvWidthHeight"
        return self.resultdata(data)

    '''
    参数下发设置超分
    '''

    def SetSuperResolution(self, key="engine.video.post_process_type", value=0):
        """ value = 0 关闭超分
            value = 1 传统超分
            value = 2 ai超分"""
        qos_para_dict = HttpUtils.get_demo_config(config.AppKey, config.Video)
        update_data = {
            key: value
        }
        qos_para_dict = HttpUtils.update_demo_config(self.platform, qos_para_dict, self.cpu, update_data)
        HttpUtils.post_demo_config(config.AppKey, data1=qos_para_dict, key=config.Video)

    def EnableSuperResolution(self, enable=True):
        data = ApiImpl.getdata()
        data["method"] = "EnableSuperResolution"
        data["enable"] = enable
        return self.resultdata(data)

    def SetH265(self, h265="1", nevc="0"):
        """
                h265=1,开启h265 h265=0,关闭h265
                nevc=1，开启nevc nevc=0,关闭nevc
                h265=0 nevc=0 ，开启h624
                h265=1 nevc=0 ，开启h265
                h265=1 nevc=1 , 开启nevc
                pc join之前，init之后
                """

        qos_para_dict = HttpUtils.get_demo_config(config.AppKey, config.Video)
        update_data = {}
        if self.platform == config.ANDROID:
            update_data = {
                "videoEncodeParam.hwh265enc": h265,
                "videoEncodeParam.h265dec": h265,
                "videoEncodeParam.h265enc": h265,
                "video.encoder.type": h265,
                "video.decoder.type": h265,
                "videoEncodeParam.nevcdec": nevc,
                "videoEncodeParam.nevcenc": nevc
            }
            data = ApiImpl.getdata()
            data["method"] = "SetH265"
            if h265 == "1":
                data["H265"] = True
            else:
                data["H265"] = False
            if nevc == "1":
                data["NEVC"] = True
            else:
                data["NEVC"] = False
            self.resultdata(data)
        elif self.platform == config.IOS:
            update_data = {
                "videoEncodeParam.hwh265enc": h265,
                "videoEncodeParam.h265dec": h265,
                "videoEncodeParam.h265enc": h265,
                "videoEncodeParam.nevcdec": nevc,
                "videoEncodeParam.nevcenc": nevc
            }
        elif self.platform == config.WINDOWS or self.platform == config.MAC:
            update_data = {
                "videoEncodeParam.h265dec": h265,
                "videoEncodeParam.h265enc": h265,
                "videoEncodeParam.nevcdec": nevc,
                "videoEncodeParam.nevcenc": nevc
            }
        qos_para_dict = HttpUtils.update_demo_config(self.platform, qos_para_dict, self.cpu, update_data)
        HttpUtils.post_demo_config(config.AppKey, data1=qos_para_dict, key=config.Video)

    def SetEnableJnd(self, enable: bool):
        update_data = {
            "engine.video.enable_jnd": enable
        }
        para_dict = HttpUtils.get_demo_config(config.AppKey, config.Video)

        para_dict = HttpUtils.update_demo_config(self.platform, para_dict, self.cpu, update_data)
        HttpUtils.post_demo_config(config.AppKey, data1=para_dict, key=config.Video)

    def ClearProfileData(self, task_cases_id: int):
        url = config.MAIN_NODE + "/es/delete_interface_data"
        HttpUtils.post(url, data1={"task_cases_id": task_cases_id})

    def GetProfileData(self, task_cases_id: int, method1: ProfileEnum, channel: str = -1, uid: int = -1):
        # url = "http://10.242.148.176:5001/demo_report/get_interface_data?task_cases_id=-1&method=onLocalVideoStats"
        if (config.SubRoomVersion):
            url = config.MAIN_NODE + """/es/getReportData?jobTaskId=%s&userId=%s&method=%s&channel_name=%s""" % (
            task_cases_id,
            uid,
            method1, channel)
        else:
            url = config.MAIN_NODE + """/es/getReportData?jobTaskId=%s&userId=%s&method=%s""" % (
            task_cases_id, uid, method1)
        data = HttpUtils.get(url)
        return data["data"]

    def InsertTestLog(self, task_cases_id: int, cases_log: str, demo_log_addr: str):
        url = config.MAIN_NODE + "/es/post_test_data"
        log_data = {
            "jobId": task_cases_id,
            "cases_log": cases_log,
            "demo_log_addr": demo_log_addr
        }
        HttpUtils.post(url, log_data)

    def GetProfileLength(self):
        data = ApiImpl.getdata()
        data["method"] = "GetProfileLength"
        return self.resultdata(data)

    # 频道管理
    def initialize(self,
                   log_level: int,
                   video_prefer_hw_encoder: bool = False,
                   video_prefer_hw_decoder: bool = False,
                   init: bool = False,
                   app_key=None,
                   is_test_observer=True,
                   log_dir="D:\\logdir\\",
                   private_address=False,
                   exnternal_render=False,
                   av_sync_is_main=False,
                   av_sync_uid=-1) -> json:
        data = ApiImpl.getdata()
        data["method"] = "initialize"
        data["log_dir_path"] = log_dir
        if config.organzation == 0:
            if app_key is None:
                data["app_key"] = ApiImpl.getAppKey()
            else:
                data["app_key"] = app_key
        elif config.organzation == 1:
            data["app_key"] = config.agora_appkey
        data["log_level"] = log_level
        data["organzation"] = config.organzation
        data["exnternal_render"] = exnternal_render
        data["av_sync_is_main"] = av_sync_is_main
        data["av_sync_uid"] = av_sync_uid
        """
        kNERtcLogLevelFatal    = 0,        /**< Fatal 级别日志信息。 */
        kNERtcLogLevelError    = 1,        /**< Error 级别日志信息。 */
        kNERtcLogLevelWarning  = 2,        /**< Warning 级别日志信息。 */
        kNERtcLogLevelInfo     = 3,        /**< Info 级别日志信息。默认级别 */
        kNERtcLogLevelDetailInfo   = 4,    /**< Detail Info 级别日志信息。 */
        kNERtcLogLevelVerbos   = 5,        /**< Verbos 级别日志信息。 */
        kNERtcLogLevelDebug    = 6,        /**< Debug 级别日志信息。如果你想获取最完整的日志，可以将日志级别设为该等级。*/
        kNERtcLogLevelOff      = 7,        /**< 不输出日志信息。*/
        """
        data["video_prefer_hw_encoder"] = video_prefer_hw_encoder
        data["video_prefer_hw_decoder"] = video_prefer_hw_decoder
        data["is_test_observer"] = is_test_observer
        data["init"] = init

        if config.remote_private_address:
            data["private_address"] = config.private_address
        else:
            if private_address:
                data["private_address"] = self.LoadPrivateAddress()

        return self.resultdata(data)

    def LoadPrivateAddress(self):
        privateJson = ""
        currentPath = os.getcwd().replace('\\', '/')
        jsonFile = currentPath + '/../PrivateAddressMobile.json'
        # if self.platform == config.IOS or self.platform == config.ANDROID:
        #     jsonFile = currentPath + '/../../../PrivateAddressMobile.json'
        # else:
        #     jsonFile = currentPath + '/PrivateAddressDesktop.json'

        print(jsonFile)
        with open(jsonFile, 'r') as f:
            privateJson = json.load(f)

        return privateJson

    def SetChannelProfile(self, profile: int):
        """
        kNERtcChannelProfileCommunication       = 0,    /**< 通话场景 */
        kNERtcChannelProfileLiveBroadcasting    = 1,    /**< 直场景 */
        """
        data = ApiImpl.getdata()
        data["method"] = "SetChannelProfile"
        data["profile"] = profile
        return self.resultdata(data)

    def JoinChannle(self, cid: str, uid: str, token: str = None, custom: str = ""):
        data = ApiImpl.getdata()
        data["method"] = "JoinChannle"
        if config.organzation == 0:
            if token is None:
                data["token"] = ""
            else:
                data["token"] = token
        elif config.organzation == 1:
            data["token"] = config.agora_token
        if self.platform == config.LINUX:
            data["channel_name"] = str(cid)
        else:
            data["channel_name"] = cid
        data["uid"] = uid
        data["custom"] = custom
        return self.resultdata(data)

    def SwitchChannel(self, cid: str, token: str = None):
        data = ApiImpl.getdata()
        data["method"] = "SwitchChannel"
        if token is None:
            data["token"] = ""
        else:
            data["token"] = token
        if self.platform == config.LINUX:
            data["channel_name"] = str(cid)
        else:
            data["channel_name"] = cid
        return self.resultdata(data)

    def Release(self):
        # self.checkPlatform(config.MAC, config.ANDROID, config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "Release"
        return self.resultdata(data)

    def LeaveChannel(self):
        data = ApiImpl.getdata()
        data["method"] = "LeaveChannel"
        return self.resultdata(data)

    def GetConnectionState(self):
        data = ApiImpl.getdata()
        data["method"] = "GetConnectionState"
        return self.resultdata(data)

    def QueryInterface(self):
        self.checkPlatform(config.MAC, config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "QueryInterface"
        return self.resultdata(data)

    # 视频管理
    '''
    开关本地视频
    '''

    def EnableLocalVideo(self, enabled: bool):
        data = ApiImpl.getdata()
        if config.organzation == 0:
            data["method"] = "EnableLocalVideo"
        else:
            data["method"] = "EnableVideo"
        data["enabled"] = enabled
        return self.resultdata(data)

    def EnableTypeLocalVideo(self, enabled: bool, type1: int):
        data = ApiImpl.getdata()
        if config.organzation == 0:
            data["method"] = "EnableTypeLocalVideo"
        else:
            data["method"] = "EnableVideo"
        data["enabled"] = enabled
        """
        0 = 主流
        1 = 辅流
        """
        data["type"] = type1
        return self.resultdata(data)

    '''
    设置视频发送配置
    可以在加入房间前或加入房间后调用此接口
    '''

    def SetVideoConfig(self,
                       maxProfile=0, cropMode=0,
                       frameRate=0, minFrameRate=0,
                       maxBitrate=0, minBitrate=0,
                       degradationPreference=0,
                       width=0,
                       height=0,
                       mirrorMode=0,
                       colorFormat=0,
                       orientationMode=0,
                       frontCamera=True,
                       channelName=-1):
        data = ApiImpl.getdata()
        if channelName != -1:
            data["method"] = "SubRoomSetLocalVideoConfig"
            data["channelName"] = channelName
        else:
            data["method"] = "SetVideoConfig"
        """
        视频编码配置。用于衡量编码质量
        kNERtcVideoProfileLowest = 0,       /**< 160x90/120, 15fps */
        kNERtcVideoProfileLow = 1,          /**< 320x180/240, 15fps */
        kNERtcVideoProfileStandard = 2,     /**< 640x360/480, 30fps */
        kNERtcVideoProfileHD720P = 3,       /**< 1280x720, 30fps */
        kNERtcVideoProfileHD1080P = 4,      /**< 1920x1080, 30fps */
        kNERtcVideoProfileNone = 5,
        """
        data["maxProfile"] = maxProfile
        """视频画面裁剪模式
        kNERtcVideoCropModeDefault = 0,     /**< Device Defalut */
        kNERtcVideoCropMode16x9    = 1,     /**< 16:9 */
        kNERtcVideoCropMode4x3     = 2,     /**< 4:3 */
        kNERtcVideoCropMode1x1     = 3,     /**< 1:1 */
        """
        data["cropMode"] = cropMode
        """
        kNERtcVideoFramerateFpsDefault  = 0,    /**< 默认帧率 */
        kNERtcVideoFramerateFps_7       = 7,    /**< 7帧每秒 */
        kNERtcVideoFramerateFps_10      = 10,   /**< 10帧每秒 */
        kNERtcVideoFramerateFps_15      = 15,   /**< 15帧每秒 */
        kNERtcVideoFramerateFps_24      = 24,   /**< 24帧每秒 */
        kNERtcVideoFramerateFps_30      = 30,   /**< 30帧每秒 */
        """
        data["frameRate"] = frameRate
        data["minFrameRate"] = minFrameRate
        data["maxBitrate"] = maxBitrate  # maxBirate 就是bitrate, 脚本变量命名问题
        data["minBitrate"] = minBitrate
        """
        kNERtcDegradationDefault            = 0,  /**< 使用引擎推荐值。通话场景使用平衡模式，直播推流场景使用清晰优先 */
        kNERtcDegradationMaintainFramerate  = 1,  /**< 帧率优先 */
        kNERtcDegradationMaintainQuality    = 2,  /**< 清晰度优先 */
        kNERtcDegradationBalanced           = 3,  /**< 平衡模式 */
        """
        data["degradationPreference"] = degradationPreference
        data["width"] = width
        data["height"] = height
        """
        mirrorMode = 0  VIDEO_MIRROR_MODE_AUTO 默认）由 SDK 决定镜像模式。
        mirrorMode = 1  VIDEO_MIRROR_MODE_ENABLED 默认）启用镜像模式。
        mirrorMode = 2  VIDEO_MIRROR_MODE_DISABLED 默认）关闭镜像模式。
        """
        data["mirrorMode"] = mirrorMode
        """
        colorFormat = 0  TEXTURE 格式
        colorFormat = 1  I420 格式
        colorFormat = 2  NV21 格式
        """
        data["colorFormat"] = colorFormat
        """
        该模式下 SDK 输出的视频方向与采集到的视频方向一致。接收端会根据收到的视频旋转信息对视频进行旋转。
        orientationMode = 0  VIDEO_OUTPUT_ORIENTATION_MODE_ADAPTATIVE 
        该模式下 SDK 固定输出横屏模式的视频。如果采集到的视频是竖屏模式，则视频编码器会对其进行裁剪。
        orientationMode = 1  VIDEO_OUTPUT_ORIENTATION_MODE_FIXED_LANDSCAPE 格式
        该模式下 SDK 固定输出竖屏模式的视频，如果采集到的视频是横屏模式，则视频编码器会对其进行裁剪。
        orientationMode = 2  VIDEO_OUTPUT_ORIENTATION_MODE_FIXED_PORTRAIT 格式
        """
        data["orientationMode"] = orientationMode
        data["frontCamera"] = frontCamera

        return self.resultdata(data)

    def SetTypeVideoConfig(self,
                           maxProfile=0, cropMode=0,
                           frameRate=0, minFrameRate=0,
                           maxBitrate=0, minBitrate=0,
                           degradationPreference=0,
                           width=0,
                           height=0,
                           mirrorMode=0,
                           colorFormat=0,
                           orientationMode=0,
                           frontCamera=True,
                           channelName=-1,
                           type1=0):
        data = ApiImpl.getdata()
        if channelName != -1:
            data["method"] = "SubRoomSetTypeLocalVideoConfig"
            data["channelName"] = channelName
        else:
            data["method"] = "SetTypeVideoConfig"
        """
        视频编码配置。用于衡量编码质量
        kNERtcVideoProfileLowest = 0,       /**< 160x90/120, 15fps */
        kNERtcVideoProfileLow = 1,          /**< 320x180/240, 15fps */
        kNERtcVideoProfileStandard = 2,     /**< 640x360/480, 30fps */
        kNERtcVideoProfileHD720P = 3,       /**< 1280x720, 30fps */
        kNERtcVideoProfileHD1080P = 4,      /**< 1920x1080, 30fps */
        kNERtcVideoProfileNone = 5,
        """
        data["maxProfile"] = maxProfile
        """视频画面裁剪模式
        kNERtcVideoCropModeDefault = 0,     /**< Device Defalut */
        kNERtcVideoCropMode16x9    = 1,     /**< 16:9 */
        kNERtcVideoCropMode4x3     = 2,     /**< 4:3 */
        kNERtcVideoCropMode1x1     = 3,     /**< 1:1 */
        """
        data["cropMode"] = cropMode
        """
        kNERtcVideoFramerateFpsDefault  = 0,    /**< 默认帧率 */
        kNERtcVideoFramerateFps_7       = 7,    /**< 7帧每秒 */
        kNERtcVideoFramerateFps_10      = 10,   /**< 10帧每秒 */
        kNERtcVideoFramerateFps_15      = 15,   /**< 15帧每秒 */
        kNERtcVideoFramerateFps_24      = 24,   /**< 24帧每秒 */
        kNERtcVideoFramerateFps_30      = 30,   /**< 30帧每秒 */
        """
        data["frameRate"] = frameRate
        data["minFrameRate"] = minFrameRate
        data["maxBitrate"] = maxBitrate  # maxBirate 就是bitrate, 脚本变量命名问题
        data["minBitrate"] = minBitrate
        """
        kNERtcDegradationDefault            = 0,  /**< 使用引擎推荐值。通话场景使用平衡模式，直播推流场景使用清晰优先 */
        kNERtcDegradationMaintainFramerate  = 1,  /**< 帧率优先 */
        kNERtcDegradationMaintainQuality    = 2,  /**< 清晰度优先 */
        kNERtcDegradationBalanced           = 3,  /**< 平衡模式 */
        """
        data["degradationPreference"] = degradationPreference
        data["width"] = width
        data["height"] = height
        """
        mirrorMode = 0  VIDEO_MIRROR_MODE_AUTO 默认）由 SDK 决定镜像模式。
        mirrorMode = 1  VIDEO_MIRROR_MODE_ENABLED 默认）启用镜像模式。
        mirrorMode = 2  VIDEO_MIRROR_MODE_DISABLED 默认）关闭镜像模式。
        """
        data["mirrorMode"] = mirrorMode
        """
        colorFormat = 0  TEXTURE 格式
        colorFormat = 1  I420 格式
        colorFormat = 2  NV21 格式
        """
        data["colorFormat"] = colorFormat
        """
        该模式下 SDK 输出的视频方向与采集到的视频方向一致。接收端会根据收到的视频旋转信息对视频进行旋转。
        orientationMode = 0  VIDEO_OUTPUT_ORIENTATION_MODE_ADAPTATIVE 
        该模式下 SDK 固定输出横屏模式的视频。如果采集到的视频是竖屏模式，则视频编码器会对其进行裁剪。
        orientationMode = 1  VIDEO_OUTPUT_ORIENTATION_MODE_FIXED_LANDSCAPE 格式
        该模式下 SDK 固定输出竖屏模式的视频，如果采集到的视频是横屏模式，则视频编码器会对其进行裁剪。
        orientationMode = 2  VIDEO_OUTPUT_ORIENTATION_MODE_FIXED_PORTRAIT 格式
        """
        data["orientationMode"] = orientationMode
        data["frontCamera"] = frontCamera
        data["type"] = type1
        return self.resultdata(data)

    def SetCameraCaptureConfig(self, height: int, width: int):
        """
        设置本地摄像头的采集偏好等配置。
        """
        data = ApiImpl.getdata()
        data["method"] = "SetCameraCaptureConfig"

        """
        preference = 0 CAPTURE_PREFERENCE_DEFAULT （默认）优先保证设备性能,
        参考用户在 setLocalVideoConfig 中设置编码器的分辨率和帧率，选择最接近的摄像头输出参数。在这种情况下，预览质量接近于编码器的输出质量。

        preference = 1 CAPTURE_PREFERENCE_MANUAL 采用用户自定义设置的摄像头输出参数
        此时用户可以通过 width 和 height 设置本地摄像头采集的视频宽高

        preference = 2 CAPTURE_PREFERENCE_OUTPUT_QUALITY 优先保证视频预览质量。
        SDK 自动设置画质较高的摄像头输出参数，提高预览画面质量。此时会消耗更多的 CPU 及内存做视频前处理。
        """
        # data["preference"] = preference
        """
        width 表示视频帧在横轴上的像素，即自定义宽
        如果您需要自定义本地采集的视频尺寸，请先将 preference 设为 CAPTURE_PREFERENCE_MANUAL，再通过Width和Height设置采集的视频宽度。
        """
        data["width"] = width
        """
        height 示视频帧在横轴上的像素，即自定义高
        如果您需要自定义本地采集的视频尺寸，请先将 preference 设为 CAPTURE_PREFERENCE_MANUAL，再通过Width Height设置采集的视频宽度。
        """
        data["height"] = height
        return self.resultdata(data)

    def SetTypeCameraCaptureConfig(self, height: int, width: int, type1: int):
        """
        设置本地摄像头的采集偏好等配置,default：0*0。
        """
        data = ApiImpl.getdata()
        data["method"] = "SetTypeCameraCaptureConfig"
        data["width"] = width
        data["height"] = height
        data["type"] = type1
        return self.resultdata(data)

    '''
    新建本地画布
    '''

    def SetupLocalVideoCanvas(self, scalingMode: int, mirrorMode=0, setBgColor: bool = False, backgroundColor: int = 0):
        """
        kNERtcVideoScaleFit      = 0,   /**< 0: 视频尺寸等比缩放。优先保证视频内容全部显示。因视频尺寸与显示视窗尺寸不一致造成的视窗未被填满的区域填充黑色。*/
        kNERtcVideoScaleFullFill = 1,   /**< 1: 视频尺寸非等比缩放。保证视频内容全部显示，且填满视窗。*/
        kNERtcVideoScaleCropFill = 2,   /**< 2: 视频尺寸等比缩放。优先保证视窗被填满。因视频尺寸与显示视窗尺寸不一致而多出的视频将被截掉。*/
        backgroundColor默认黑色，Android端不支持背景颜色参数设置，其他端支持'''
        """
        data = ApiImpl.getdata()
        data["method"] = "SetupLocalVideoCanvas"
        data["scalingMode"] = scalingMode
        if setBgColor:
            data["backgroundColor"] = backgroundColor
        # ios 生效
        data["mirrorMode"] = mirrorMode
        return self.resultdata(data)

    def SetupRemoteVideoCanvas(self, userId: str, scalingMode: int, mirrorMode=0, setBgColor: bool = False,
                               backgroundColor: int = 0):
        '''backgroundColor默认黑色，Android端不支持背景颜色参数设置，其他端支持'''
        data = ApiImpl.getdata()
        data["method"] = "SetupRemoteVideoCanvas"
        data["scalingMode"] = scalingMode
        data["userId"] = userId
        if setBgColor:
            data["backgroundColor"] = backgroundColor
        # ios 生效
        data["mirrorMode"] = mirrorMode
        return self.resultdata(data)

    def SetLocalRenderMode(self, scalingMode: int, mirrorMode: int = 0):
        # if self.platform != config.ANDROID:
        data = ApiImpl.getdata()
        data["method"] = "SetLocalRenderMode"
        data["scalingMode"] = scalingMode
        # android  0是关闭镜像，其他值 开启镜像
        data["mirrorMode"] = mirrorMode
        return self.resultdata(data)

    def SetLocalSubStreamRenderMode(self, scalingMode: int):
        data = ApiImpl.getdata()
        data["method"] = "SetLocalSubStreamRenderMode"
        data["scalingMode"] = scalingMode
        return self.resultdata(data)

    def SetRemoteRenderMode(self, userId: str, scalingMode: int):
        data = ApiImpl.getdata()
        data["method"] = "SetRemoteRenderMode"
        data["userId"] = userId
        data["scalingMode"] = scalingMode
        return self.resultdata(data)

    def SetRemoteSubStreamRenderMode(self, userId: str, scalingMode: int):
        data = ApiImpl.getdata()
        data["method"] = "SetRemoteSubStreamRenderMode"
        data["userId"] = userId
        data["scalingMode"] = scalingMode
        return self.resultdata(data)

    def StartVideoPreview(self):
        data = ApiImpl.getdata()
        data["method"] = "StartVideoPreview"
        return self.resultdata(data)

    def StartTypeVideoPreview(self, type1: int, index=0):
        data = ApiImpl.getdata()
        data["method"] = "StartTypeVideoPreview"
        data["type"] = type1
        data["index"] = index
        return self.resultdata(data)

    def StopVideoPreview(self):
        data = ApiImpl.getdata()
        data["method"] = "StopVideoPreview"
        return self.resultdata(data)

    def StopTypeVideoPreview(self, type1: int):
        data = ApiImpl.getdata()
        data["method"] = "StopTypeVideoPreview"
        data["type"] = type1
        return self.resultdata(data)

    def MuteLocalVideoStream(self, mute: bool):
        data = ApiImpl.getdata()
        data["method"] = "MuteLocalVideoStream"
        data["mute"] = mute
        return self.resultdata(data)

    def MuteLocalTypeVideoStream(self, mute: bool, type1: int):
        data = ApiImpl.getdata()
        data["method"] = "MuteLocalTypeVideoStream"
        data["mute"] = mute
        data["type"] = type1
        return self.resultdata(data)

    def SubscribeRemoteVideoStream(self, uid: str, subscribe: bool, streamType: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeRemoteVideoStream"
        data["uid"] = uid
        data["subscribe"] = subscribe
        """
        kNERtcRemoteVideoStreamTypeHigh     = 0, /**< 默认大流 */
        kNERtcRemoteVideoStreamTypeLow      = 1, /**< 小流 */
        kNERtcRemoteVideoStreamTypeNone     = 2, /**< 不订阅 */
        """
        data["streamType"] = streamType
        return self.resultdata(data)

    def SubscribeRemoteVideoSubStream(self, uid: str, subscribe: bool):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeRemoteVideoSubStream"
        data["uid"] = uid
        data["subscribe"] = subscribe
        return self.resultdata(data)

    def SetLocalVideoMirrorMode(self, mirrorMode: int):
        """
        kNERtcVideoMirrorModeAuto       = 0,    /**< 0: （默认）Windows/macOS SDK 启用镜像模式。在 iOS/Android 平台中：如果你使用前置摄像头，SDK 默认启用镜像模式；如果你使用后置摄像头，SDK 默认关闭镜像模式。*/
        kNERtcVideoMirrorModeEnabled    = 1,    /**< 1: 启用镜像模式。*/
        kNERtcVideoMirrorModeDisabled   = 2,    /**< 2: 关闭镜像模式。*/
        """
        self.checkPlatform(config.WINDOWS, config.MAC, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVideoMirrorMode"
        data["damirrorModeta"] = mirrorMode
        return self.resultdata(data)

    def SetOtherParameters(self,
                           record_host_enabled=False,
                           record_audio_enabled=False,
                           record_video_enabled=False,
                           record_type=0,
                           auto_subscribe_audio=True,
                           publish_self_stream_enabled=False,
                           log_level=3,
                           audio_processing_aec_enable=False,
                           audio_processing_agc_enable=False,
                           audio_processing_ns_enable=False,
                           audio_processing_external_audiomix_enable=False,
                           audio_processing_earphone=False,
                           video_sendonpub_type=1,
                           auto_start_local_audio=True,
                           auto_start_local_video=True,
                           test_1v1=False,
                           is_debug_server=True):
        self.checkPlatform(config.LINUX, config.ELECTRON)
        # 设置默认参数
        """
        "record_host_enabled"          /**< bool value. true: 录制主讲人, false: 不是录制主讲人 */
        "record_audio_enabled"         /**< bool value，启用服务器音频录制。默认值 true */
        "record_video_enabled"         /**< bool value，启用服务器视频录制。默认值 true */
        "record_type"                  /**< int value, NERtcRecordType */
        "auto_subscribe_audio"         /**< bool value，其他用户打开音频时，自动订阅。 默认值 true */
        "publish_self_stream_enabled"   /**< bool value，开启旁路直播。默认值 false */
        "log_level"                     /**< int value, NERtcLogLevel，SDK 输出小于或等于该级别的log，默认为 kNERtcLogLevelInfo */
        "audio_processing_aec_enable"   /**< bool value. AEC开关，默认值 true */
        "audio_processing_agc_enable"   /**< bool value. AGC开关，默认值 true */
        "audio_processing_ns_enable"   /**< bool value. NS开关，默认值 true */
        "audio_processing_external_audiomix_enable"   /**< bool value. 输入混音开关，默认值 false */
        "audio_processing_earphone"    /**< bool value. 通知SDK是否使用耳机， true: 使用耳机, false: 不使用耳机，默认值 false */
        "video_sendonpub_type"      /**< int value. NERtcSendOnPubType；设置视频发送策略，默认发送大流 kNERtcSendOnPubHigh；通话前设置有效 */
        """
        data = ApiImpl.getdata()
        data["method"] = "SetParameters"
        data["record_host_enabled"] = record_host_enabled
        data["record_audio_enabled"] = record_audio_enabled
        data["record_video_enabled"] = record_video_enabled
        """
        kNERtcRecordTypeAll = 0,    /**< 参与混合录制且录制单人文件。*/
        kNERtcRecordTypeMix = 1,    /**< 参与混合录制。*/
        kNERtcRecordTypeSingle = 2, /**< 只录单人文件。*/
        """
        data["record_type"] = record_type
        data["auto_subscribe_audio"] = auto_subscribe_audio
        data["publish_self_stream_enabled"] = publish_self_stream_enabled
        """
        kNERtcLogLevelFatal    = 0,        /**< Fatal 级别日志信息。 */
        kNERtcLogLevelError    = 1,        /**< Error 级别日志信息。 */
        kNERtcLogLevelWarning  = 2,        /**< Warning 级别日志信息。 */
        kNERtcLogLevelInfo     = 3,        /**< Info 级别日志信息。默认级别 */
        kNERtcLogLevelDetailInfo   = 4,    /**< Detail Info 级别日志信息。 */
        kNERtcLogLevelVerbos   = 5,        /**< Verbos 级别日志信息。 */
        kNERtcLogLevelDebug    = 6,        /**< Debug 级别日志信息。如果你想获取最完整的日志，可以将日志级别设为该等级。*/
        kNERtcLogLevelOff      = 7,        /**< 不输出日志信息。*/
        """
        data["log_level"] = log_level
        data["audio_processing_aec_enable"] = audio_processing_aec_enable
        data["audio_processing_agc_enable"] = audio_processing_agc_enable
        data["audio_processing_ns_enable"] = audio_processing_ns_enable
        data["audio_processing_external_audiomix_enable"] = audio_processing_external_audiomix_enable
        data["audio_processing_earphone"] = audio_processing_earphone
        """
        kNERtcSendOnPubNone = 0, /**< 不主动发送数据流，被订阅后发送。 */
        kNERtcSendOnPubHigh = 1, /**< 主动发送大流。 */
        kNERtcSendOnPubLow = 1 << 1, /**< 主动发送小流。 */
        kNERtcSendOnPubAll = kNERtcSendOnPubLow | kNERtcSendOnPubHigh, /**< 主动发送大小流。 */
        """
        data["video_sendonpub_type"] = video_sendonpub_type

        """
        auto_start_local_audio = True 自动开音频
        auto_start_local_video = True 自动开视频
        """
        data["auto_start_local_audio"] = auto_start_local_audio
        data["auto_start_local_video"] = auto_start_local_video
        data["test_1v1"] = test_1v1
        data["is_debug_server"] = is_debug_server
        return self.resultdata(data)

    def SetParameters(self,
                      record_host_enabled=False,
                      record_audio_enabled=False,
                      record_video_enabled=False,
                      record_type=0,
                      auto_subscribe_audio=True,
                      publish_self_stream_enabled=False,
                      log_level=3,
                      audio_processing_aec_enable=True,
                      audio_processing_agc_enable=True,
                      audio_processing_ns_enable=True,
                      audio_processing_external_audiomix_enable=False,
                      audio_processing_earphone=False,
                      video_sendonpub_type=1,
                      auto_start_local_audio=True,
                      auto_start_local_video=True,
                      test_1v1=False,
                      is_debug_server=True,
                      auto_subscribe_video: bool = False,
                      drop_bandwidth_enabled: bool = False):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX)
        # 设置默认参数
        """
        "record_host_enabled"          /**< bool value. true: 录制主讲人, false: 不是录制主讲人 */
        "record_audio_enabled"         /**< bool value，启用服务器音频录制。默认值 true */
        "record_video_enabled"         /**< bool value，启用服务器视频录制。默认值 true */
        "record_type"                  /**< int value, NERtcRecordType */
        "auto_subscribe_audio"         /**< bool value，其他用户打开音频时，自动订阅。 默认值 true */
        "publish_self_stream_enabled"   /**< bool value，开启旁路直播。默认值 false */
        "log_level"                     /**< int value, NERtcLogLevel，SDK 输出小于或等于该级别的log，默认为 kNERtcLogLevelInfo */
        "audio_processing_aec_enable"   /**< bool value. AEC开关，默认值 true */
        "audio_processing_agc_enable"   /**< bool value. AGC开关，默认值 true */
        "audio_processing_ns_enable"   /**< bool value. NS开关，默认值 true */
        "audio_processing_external_audiomix_enable"   /**< bool value. 输入混音开关，默认值 false */
        "audio_processing_earphone"    /**< bool value. 通知SDK是否使用耳机， true: 使用耳机, false: 不使用耳机，默认值 false */
        "video_sendonpub_type"      /**< int value. NERtcSendOnPubType；设置视频发送策略，默认发送大流 kNERtcSendOnPubHigh；通话前设置有效 */
        """
        data = ApiImpl.getdata()
        data["method"] = "SetParameters"
        data["record_host_enabled"] = record_host_enabled
        data["record_audio_enabled"] = record_audio_enabled
        data["record_video_enabled"] = record_video_enabled
        """
        kNERtcRecordTypeAll = 0,    /**< 参与混合录制且录制单人文件。*/
        kNERtcRecordTypeMix = 1,    /**< 参与混合录制。*/
        kNERtcRecordTypeSingle = 2, /**< 只录单人文件。*/
        """
        data["record_type"] = record_type
        data["auto_subscribe_audio"] = auto_subscribe_audio
        data["publish_self_stream_enabled"] = publish_self_stream_enabled
        """
        kNERtcLogLevelFatal    = 0,        /**< Fatal 级别日志信息。 */
        kNERtcLogLevelError    = 1,        /**< Error 级别日志信息。 */
        kNERtcLogLevelWarning  = 2,        /**< Warning 级别日志信息。 */
        kNERtcLogLevelInfo     = 3,        /**< Info 级别日志信息。默认级别 */
        kNERtcLogLevelDetailInfo   = 4,    /**< Detail Info 级别日志信息。 */
        kNERtcLogLevelVerbos   = 5,        /**< Verbos 级别日志信息。 */
        kNERtcLogLevelDebug    = 6,        /**< Debug 级别日志信息。如果你想获取最完整的日志，可以将日志级别设为该等级。*/
        kNERtcLogLevelOff      = 7,        /**< 不输出日志信息。*/
        """
        data["log_level"] = log_level
        data["audio_processing_aec_enable"] = audio_processing_aec_enable
        data["audio_processing_agc_enable"] = audio_processing_agc_enable
        data["audio_processing_ns_enable"] = audio_processing_ns_enable
        data["audio_processing_external_audiomix_enable"] = audio_processing_external_audiomix_enable
        data["audio_processing_earphone"] = audio_processing_earphone
        """
        kNERtcSendOnPubNone = 0, /**< 不主动发送数据流，被订阅后发送。 */
        kNERtcSendOnPubHigh = 1, /**< 主动发送大流。 */
        kNERtcSendOnPubLow = 1 << 1, /**< 主动发送小流。 */
        kNERtcSendOnPubAll = kNERtcSendOnPubLow | kNERtcSendOnPubHigh, /**< 主动发送大小流。 */
        """
        data["video_sendonpub_type"] = video_sendonpub_type

        """
        auto_start_local_audio = True 自动开音频
        auto_start_local_video = True 自动开视频
        """
        data["auto_start_local_audio"] = auto_start_local_audio
        data["auto_start_local_video"] = auto_start_local_video
        data["test_1v1"] = test_1v1
        data["is_debug_server"] = is_debug_server
        data["auto_subscribe_video"] = auto_subscribe_video
        data["drop_bandwidth_enabled"] = drop_bandwidth_enabled
        return self.resultdata(data)

    def IosSetParameters(self,
                         video_prefer_hw_encoder: bool = True,
                         video_prefer_hw_decoder: bool = True,
                         video_capture_observer_enabled: bool = False,
                         video_start_with_back_camera: bool = False,
                         video_prefer_metal_render: bool = False,
                         video_sendonpub_type: int = 1,
                         auto_subscribe_audio: bool = True,
                         record_host_enabled: bool = False,
                         record_audio_enabled: bool = False,
                         record_video_enabled: bool = False,
                         record_type: int = 0,
                         publish_self_stream_enabled: bool = False,
                         log_level: int = 3,
                         audio_processing_aec_enable=False,
                         audio_processing_agc_enable=False,
                         audio_processing_ns_enable=False,
                         test_1v1=False,
                         is_debug_server=True,
                         auto_subscribe_video: bool = True,
                         drop_bandwidth_enabled: bool = False
                         ):
        self.checkPlatform(config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "SetParameters"
        data["video_prefer_hw_encoder"] = video_prefer_hw_encoder
        data["video_prefer_hw_decoder"] = video_prefer_hw_decoder
        data["video_capture_observer_enabled"] = video_capture_observer_enabled
        data["video_start_with_back_camera"] = video_start_with_back_camera
        data["video_prefer_metal_render"] = video_prefer_metal_render
        data["video_sendonpub_type"] = video_sendonpub_type
        data["auto_subscribe_audio"] = auto_subscribe_audio
        data["record_host_enabled"] = record_host_enabled
        data["record_audio_enabled"] = record_audio_enabled
        data["record_video_enabled"] = record_video_enabled
        data["record_type"] = record_type
        data["publish_self_stream_enabled"] = publish_self_stream_enabled
        data["log_level"] = log_level

        data["audio_processing_aec_enable"] = audio_processing_aec_enable
        data["audio_processing_agc_enable"] = audio_processing_agc_enable
        data["audio_processing_ns_enable"] = audio_processing_ns_enable
        data["test_1v1"] = test_1v1
        data["is_debug_server"] = is_debug_server
        data["auto_subscribe_video"] = auto_subscribe_video
        data["drop_bandwidth_enabled"] = drop_bandwidth_enabled  # 设置True才是不降带宽
        return self.resultdata(data)

    def AosSetParameters(self,
                         video_prefer_hw_encoder: bool = False,
                         video_prefer_hw_decoder: bool = False,
                         video_start_with_back_camera: bool = False,
                         video_sendonpub_type: int = 1,
                         auto_subscribe_audio: bool = True,
                         record_host_enabled: bool = False,
                         record_audio_enabled: bool = False,
                         record_video_enabled: bool = False,
                         record_type: int = 0,
                         publish_self_stream_enabled: bool = False,
                         audio_processing_aec_enable=True,
                         audio_processing_agc_enable=True,
                         audio_processing_ns_enable=True,
                         audio_processing_external_audiomix_enable=False,
                         audio_processing_earphone=False,
                         quic_url=None,
                         media_url=None,
                         test_1v1=False,
                         is_debug_server=True,
                         auto_subscribe_video: bool = True,
                         drop_bandwidth_enabled: bool = False
                         ):
        self.checkPlatform(config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SetParameters"
        data["video_prefer_hw_encoder"] = video_prefer_hw_encoder
        data["video_prefer_hw_decoder"] = video_prefer_hw_decoder
        data["video_start_with_back_camera"] = video_start_with_back_camera
        data["video_sendonpub_type"] = video_sendonpub_type
        data["auto_subscribe_audio"] = auto_subscribe_audio
        data["record_host_enabled"] = record_host_enabled
        data["record_audio_enabled"] = record_audio_enabled
        data["record_video_enabled"] = record_video_enabled
        data["record_type"] = record_type
        data["publish_self_stream_enabled"] = publish_self_stream_enabled
        data["audio_processing_aec_enable"] = audio_processing_aec_enable
        data["audio_processing_agc_enable"] = audio_processing_agc_enable
        data["audio_processing_ns_enable"] = audio_processing_ns_enable
        data["audio_processing_external_audiomix_enable"] = audio_processing_external_audiomix_enable
        data["audio_processing_earphone"] = audio_processing_earphone
        if media_url is not None:
            data["media_url"] = media_url
        if quic_url is not None:
            data["quic_url"] = quic_url
        data["test_1v1"] = test_1v1
        data["is_debug_server"] = is_debug_server
        data["auto_subscribe_video"] = auto_subscribe_video
        data["drop_bandwidth_enabled"] = drop_bandwidth_enabled
        return self.resultdata(data)

    def GetParameters(self, key: str, extra_info: str):
        data = ApiImpl.getdata()
        data["method"] = "GetParameters"
        data["key"] = key
        data["extraInfo"] = extra_info
        return self.resultdata(data)

    def EnableAPMMonitor(self, enable: bool):
        '''性能数据开关'''
        data = ApiImpl.getdata()
        data["method"] = "EnableAPMMonitor"
        data["enable"] = enable
        return self.resultdata(data)

    def SetPrivateParams(self, private_params: str):
        data = ApiImpl.getdata()
        data["method"] = "SetPrivateParams"
        data["private_params"] = private_params

        return self.resultdata(data)

    # Marvel
    '''
    enable: YES, 开启内存监测
    enable: NO, 清空之前内存快照
    '''

    def EnableMarvelOOMDetector(self, enable: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "EnableMarvelOOMDetector"
        data["enable"] = enable

        return self.resultdata(data)

    '''
    上传最近一个 EnableMarvelOOMDetector 为 True 到现在的内存使用， 建议在怀疑有内存泄露的地方，隔2～3 分钟内存稳定后再上报
    '''

    def ReportMarvelReportData(self, issue: str = "", customInfo: str = ""):
        data = ApiImpl.getdata()
        data["method"] = "ReportMarvelReportData"
        data["issue"] = issue
        data["customInfo"] = customInfo

        return self.resultdata(data)

    # 音频管理
    def EnableLocalAudio(self, enabled: bool):
        data = ApiImpl.getdata()
        data["method"] = "EnableLocalAudio"
        data["enabled"] = enabled
        return self.resultdata(data)

    def SetAudioProfile(self, audioProfile: int, audioScene: int):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioProfile"
        """
        kNERtcAudioProfileDefault = 0,              /**< 0: 默认设置。Speech场景下为 kNERtcAudioProfileStandardExtend，Music场景下为 kNERtcAudioProfileHighQuality */
        kNERtcAudioProfileStandard = 1,             /**< 1: 普通质量的音频编码，16000Hz，20Kbps */
        kNERtcAudioProfileStandardExtend = 2,       /**< 2: 普通质量的音频编码，16000Hz，32Kbps */
        kNERtcAudioProfileMiddleQuality = 3,        /**< 3: 中等质量的音频编码，48000Hz，32Kbps */
        kNERtcAudioProfileMiddleQualityStereo = 4,  /**< 4: 中等质量的立体声编码，4800
        0Hz * 2，64Kbps  */
        kNERtcAudioProfileHighQuality = 5,          /**< 5: 高质量的音频编码，48000Hz，64Kbps  */
        kNERtcAudioProfileHighQualityStereo = 6,    /**< 6: 高质量的立体声编码，48000Hz * 2，128Kbps  */
        """
        data["audioProfile"] = audioProfile
        """
        kNERtcAudioScenarioDefault  = 0,    /** 0: 默认设置:kNERtcChannelProfileCommunication下为kNERtcAudioScenarioSpeech，kNERtcChannelProfileLiveBroadcasting下为kNERtcAudioScenarioMusic。 */
        kNERtcAudioScenarioSpeech   = 1,    /** 1: 语音场景. NERtcAudioProfileType 推荐使用 kNERtcAudioProfileMiddleQuality 及以下 */
        kNERtcAudioScenarioMusic    = 2,    /** 2: 音乐场景。NERtcAudioProfileType 推荐使用 kNERtcAudioProfileMiddleQualityStereo 及以上 */
        int RtcAudioScenarioChatRoom = 3;
        """
        data["audioScene"] = audioScene
        return self.resultdata(data)

    def SetLocalVoiceEqualizationPreset(self, bandFrequency: int, bandGain: int):
        # 均衡器
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVoiceEqualization"
        """
        kNERtcVoiceEqualizationOff(-1),
        kNERtcVoiceEqualizationDeep(0),
        kNERtcVoiceEqualizationMellow(1),
        kNERtcVoiceEqualizationClear(2);
        """
        data["bandGain"] = bandGain
        data["bandFrequency"] = bandFrequency
        return self.resultdata(data)

    def SetLocalVoicePitch(self, pitch: float):
        # 均衡器
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVoicePitch"
        """
        pitch   语音频率。可以在 [0.5, 2.0] 范围内设置。取值越小，则音调越低
        """
        data["pitch"] = pitch
        return self.resultdata(data)

    def SetLocalVoiceReverbPreset(self, which: int):
        # 混响
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVoiceReverbPreset"
        """
        kNERtcVoiceReverbOff(-1),
        kNERtcVoiceReverbKTV(0),
        kNERtcVoiceReverbRecite(1);
        """
        data["which"] = which
        return self.resultdata(data)

    def SetLocalVoiceChangerPreset(self, which: int):
        # 变声
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVoiceChangerPreset"
        """
        kNERtcVoiceChangerOff(-1),
        kNERtcVoiceChangerRobot(0),
        kNERtcVoiceChangerGaint(1)
        kNERtcVoiceChangerChurchecho(2),
        kNERtcVoiceChangerHorror(3),
        kNERtcVoiceChangerMuffled(4),
        kNERtcVoiceChangerManToWoman(5),
        kNERtcVoiceChangerWomanToMan(6),
        kNERtcVoiceChangerManToLoli(7),
        kNERtcVoiceChangerWomanToLoli(8);
        """
        data["which"] = which
        return self.resultdata(data)

    def SetVoiceBeautifierPreset(self, which: int):
        # 美声效果
        data = ApiImpl.getdata()
        data["method"] = "SetVoiceBeautifierPreset"
        """
        kNERtcVoiceBeautifierOff 默认关闭
        kNERtcVoiceBeautifierMuffled 低沉
        kNERtcVoiceBeautifierMellow 圆润
        kNERtcVoiceBeautifierClear  清澈

        kNERtcVoiceBeautifierMagnetic 磁性
        kNERtcVoiceBeautifierRecordingstudio 录音棚
        kNERtcVoiceBeautifierNature 天籁
        kNERtcVoiceBeautifierKTV KTV

        kNERtcVoiceBeautifierRemote 悠远
        kNERtcVoiceBeautifierChurch 教堂
        kNERtcVoiceBeautifierBedroom 卧室
        kNERtcVoiceBeautifierLive Live
        """
        data["which"] = which
        return self.resultdata(data)

    def MuteLocalAudioStream(self, audioMuted: bool):
        data = ApiImpl.getdata()
        data["method"] = "MuteLocalAudioStream"
        data["audioMuted"] = audioMuted
        return self.resultdata(data)

    def SubscribeRemoteAudioStream(self, uid: int, subscribe: bool):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeRemoteAudioStream"
        if self.platform == config.LINUX:
            data["uid"] = str(uid)
        else:
            data["uid"] = uid
        data["subscribe"] = subscribe
        return self.resultdata(data)

    def AdjustRecordingSignalVolume(self, volume: int):
        # self.checkPlatform(config.IOS, config.ANDROID, config.WINDOWS)
        data = ApiImpl.getdata()
        data["method"] = "AdjustRecordingSignalVolume"
        data["volume"] = volume
        return self.resultdata(data)

    def AdjustPlaybackSignalVolume(self, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "AdjustPlaybackSignalVolume"
        data["volume"] = volume
        return self.resultdata(data)

    def AdjustUserPlaybackSignalVolume(self, volume: int, uid: int):
        data = ApiImpl.getdata()
        data["method"] = "AdjustUserPlaybackSignalVolume"
        data["volume"] = volume
        data["uid"] = uid
        return self.resultdata(data)

    def SubscribeAllRemoteAudio(self, enabled: bool):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeAllRemoteAudio"
        data["enabled"] = enabled
        return self.resultdata(data)

    # 音频辅流
    def EnableLocalSubStreamAudio(self, enabled: bool):
        data = ApiImpl.getdata()
        data["method"] = "EnableLocalSubStreamAudio"
        data["enabled"] = enabled
        return self.resultdata(data)

    def SubscribeRemoteSubStreamAudio(self, uid: int, subscribe: bool):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeRemoteSubStreamAudio"
        data["uid"] = uid
        data["subscribe"] = subscribe
        return self.resultdata(data)

    def MuteLocalSubStreamAudio(self, mute: bool):
        data = ApiImpl.getdata()
        data["method"] = "MuteLocalSubStreamAudio"
        data["mute"] = mute
        return self.resultdata(data)

    def SetExternalSubStreamAudioSource(self, enabled: bool, sampleRate: int, channels: int):
        data = ApiImpl.getdata()
        data["method"] = "SetExternalSubStreamAudioSource"
        data["enable"] = enabled
        data["sampleRate"] = sampleRate
        data["channels"] = channels
        return self.resultdata(data)

    def PushExternalSubStreamAudioFrame(self, audio_type: int, sampleRate: int, channels: int, bytes_per_sample: int,
                                        samples_per_channel: int, path: str, enable: bool = False,
                                        disableExternal=False):
        data = ApiImpl.getdata()
        data["method"] = "PushExternalSubStreamAudioFrame"
        data["type"] = audio_type
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["bytes_per_sample"] = bytes_per_sample
        data["samples_per_channel"] = samples_per_channel
        data["path"] = path
        data["enable"] = enable
        data["disableExternal"] = disableExternal
        return self.resultdata(data)

    # 屏幕共享
    def StartScreenCaptureByDisplayId(self, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        """#通过屏幕 ID 共享屏幕，该方法仅适用于 macOS"""
        self.checkPlatform(config.MAC)
        data = ApiImpl.getdata()
        data["method"] = "StartScreenCaptureByDisplayId"
        data["profile"] = profile
        data["bitrate"] = bitrate
        data["frameRate"] = frameRate
        data["width"] = width
        data["height"] = height
        data["prefer"] = prefer
        return self.resultdata(data)

    def StartScreenCaptureByWindowId(self, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "StartScreenCaptureByWindowId"
        ''' profile 取值0,1,2，3， 3是自定义分辨率
        kNERtcScreenProfile480P     640x480, 5fps

        kNERtcScreenProfileHD720P   1280x720, 5fps

        kNERtcScreenProfileHD1080P  1920x1080, 5fps。默认

        kNERtcScreenProfileCustom   自定义

        kNERtcScreenProfileNone     无效果。

        kNERtcScreenProfileMAX  1920x1080, 5fps。
        '''
        data["profile"] = profile
        '''共享视频的码率，单位为 kbps；默认值为 0，表示 SDK 根据当前共享屏幕的分辨率计算出一个合理的值'''
        data["bitrate"] = bitrate
        '''共享视频的帧率，kNERtcScreenProfileCustom下生效，单位为 fps；默认值为 5，建议不要超过 15。'''
        data["frameRate"] = frameRate
        '''屏幕共享视频发送的最大像素值，kNERtcScreenProfileCustom下生效。'''
        data["width"] = width
        data["height"] = height
        '''
        屏幕共享功能的编码策略倾向
        0 kNERtcSubStreamContentPreferMotion: 内容类型为动画
        1 kNERtcSubStreamContentPreferDetails: 内容类型为细节
        '''
        data["prefer"] = prefer
        return self.resultdata(data)

    '''使用方式参考上面的方法'''

    def StartScreenCaptureByScreenRect(self, profile=1, bitrate=0, frameRate=5, width=0, height=0, prefer=0):
        """该方法仅适用于 Windows。"""
        self.checkPlatform(config.WINDOWS, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "StartScreenCaptureByScreenRect"
        data["profile"] = profile
        data["bitrate"] = bitrate
        data["frameRate"] = frameRate
        data["width"] = width
        data["height"] = height
        data["prefer"] = prefer
        return self.resultdata(data)

    def StartScreenCapture(self, profile=1, bitrate=0, frameRate=5, prefer=0):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "StartScreenCapture"
        data["maxProfile"] = profile
        data["bitrate"] = bitrate
        data["frameRate"] = frameRate
        """0动画模式 1 细节模式"""
        data["prefer"] = prefer
        return self.resultdata(data)

    def PauseScreenCapture(self):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "PauseScreenCapture"
        return self.resultdata(data)

    def ResumeScreenCapture(self):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "ResumeScreenCapture"
        return self.resultdata(data)

    def UpdateScreenCaptureRegion(self, x: int = 100, y: int = 200, width: int = 100, height: int = 200):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX, config.ELECTRON)
        data = ApiImpl.getdata()
        data["method"] = "UpdateScreenCaptureRegion"
        data["x"] = x
        data["y"] = y
        data["width"] = width
        data["height"] = height
        return self.resultdata(data)

    def StopScreenCapture(self):
        self.checkPlatform(config.MAC, config.WINDOWS, config.LINUX, config.ELECTRON, config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "StopScreenCapture"
        return self.resultdata(data)

    def EnableDualStreamMode(self, enabled: bool):
        data = ApiImpl.getdata()
        data["method"] = "EnableDualStreamMode"
        data["enable"] = enabled
        return self.resultdata(data)

    def StartAudioMixing(self, path="http://mpge.5nd.com/2015/2015-11-26/69708/1.mp3", loopCount: int = 1,
                         sendEnabled=True, playbackEnabled=True, sendVolume=100, playbackVolume=100,
                         startTime=0, audioType: int = 0, progressInterval=0):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioMixing"
        data["path"] = path
        data["loopCount"] = loopCount
        data["sendEnabled"] = sendEnabled
        data["playbackEnabled"] = playbackEnabled
        data["sendVolume"] = sendVolume
        data["playbackVolume"] = playbackVolume
        data["startTime"] = startTime
        data["audioType"] = audioType
        data["progressInterval"] = progressInterval
        return self.resultdata(data)

    def PlayOnlineAudioMixing(self, url: str, loop: int = 1,
                              sendEnabled=True, playbackEnabled=True, sendVolume=100, playbackVolume=100):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioMixing"
        data["path"] = url
        data["loopCount"] = loop
        data["sendEnabled"] = sendEnabled
        data["playbackEnabled"] = playbackEnabled
        data["sendVolume"] = sendVolume
        data["playbackVolume"] = playbackVolume
        return self.resultdata(data)

    def StopAudioMixing(self):
        data = ApiImpl.getdata()
        data["method"] = "StopAudioMixing"
        return self.resultdata(data)

    def PauseAudioMixing(self):
        data = ApiImpl.getdata()
        data["method"] = "PauseAudioMixing"
        return self.resultdata(data)

    def ResumeAudioMixing(self):
        data = ApiImpl.getdata()
        data["method"] = "ResumeAudioMixing"
        return self.resultdata(data)

    def SetAudioMixingPlaybackVolume(self, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioMixingPlaybackVolume"
        data["volume"] = volume
        return self.resultdata(data)

    def SetAudioMixingSendVolume(self, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioMixingSendVolume"
        data["volume"] = volume
        return self.resultdata(data)

    def GetAudioMixingPlaybackVolume(self):
        data = ApiImpl.getdata()
        data["method"] = "GetAudioMixingPlaybackVolume"
        return self.resultdata(data)

    def GetAudioMixingSendVolume(self):
        data = ApiImpl.getdata()
        data["method"] = "GetAudioMixingSendVolume"
        return self.resultdata(data)

    def GetAudioMixingDuration(self):
        data = ApiImpl.getdata()
        data["method"] = "GetAudioMixingDuration"
        return self.resultdata(data)

    def GetAudioMixingCurrentPosition(self):
        data = ApiImpl.getdata()
        data["method"] = "GetAudioMixingCurrentPosition"
        return self.resultdata(data)

    def SetAudioMixingPosition(self, position: int):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioMixingPosition"
        data["position"] = position
        return self.resultdata(data)

    def GetEffectPlaybackVolume(self, effect_id: int):
        data = ApiImpl.getdata()
        data["method"] = "GetEffectPlaybackVolume"
        data["effect_id"] = effect_id
        return self.resultdata(data)

    def SetEffectPlaybackVolume(self, effect_id: int, volume=100):
        data = ApiImpl.getdata()
        data["method"] = "SetEffectPlaybackVolume"
        data["effect_id"] = effect_id
        data["volume"] = volume
        return self.resultdata(data)

    def PlayEffect(self, effect_id: int, loopCount=1, playbackEnabled=True, sendEnable=True, sendVolume=50,
                   playbackVolume=100, startTime=0, audioType: int = 0, progressInterval=0):
        data = ApiImpl.getdata()
        data["method"] = "PlayEffect"
        data["effect_id"] = effect_id
        data["loopCount"] = loopCount
        data["playbackEnabled"] = loopCount
        data["playbackVolume"] = playbackVolume
        data["sendEnabled"] = sendEnable
        data["sendVolume"] = sendVolume
        data["startTime"] = startTime
        data["audioType"] = audioType
        data["progressInterval"] = progressInterval
        return self.resultdata(data)

    def StopEffect(self, effect_id: int):
        data = ApiImpl.getdata()
        data["method"] = "StopEffect"
        data["effect_id"] = effect_id
        return self.resultdata(data)

    def StopAllEffects(self):
        data = ApiImpl.getdata()
        data["method"] = "StopAllEffects"
        return self.resultdata(data)

    def PauseEffect(self, effect_id: int):
        data = ApiImpl.getdata()
        data["method"] = "PauseEffect"
        data["effect_id"] = effect_id
        return self.resultdata(data)

    def PauseAllEffects(self):
        data = ApiImpl.getdata()
        data["method"] = "PauseAllEffects"
        return self.resultdata(data)

    def ResumeEffect(self, effect_id: int):
        data = ApiImpl.getdata()
        data["method"] = "ResumeEffect"
        data["effect_id"] = effect_id
        return self.resultdata(data)

    def ResumeAllEffects(self):
        data = ApiImpl.getdata()
        data["method"] = "ResumeAllEffects"
        return self.resultdata(data)

    def SetEffectSendVolume(self, effect_id: int, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "SetEffectSendVolume"
        data["effect_id"] = effect_id
        data["volume"] = volume
        return self.resultdata(data)

    def GetEffectSendVolume(self, effect_id: int):
        data = ApiImpl.getdata()
        data["method"] = "GetEffectSendVolume"
        data["effect_id"] = effect_id
        return self.resultdata(data)

    def EnableAudioVolumeIndication(self, enable: bool, interval: int):
        # interval 指定音量提示的时间间隔，单位为毫秒。必须设置为 100 毫秒的整数倍值。
        data = ApiImpl.getdata()
        data["method"] = "EnableAudioVolumeIndication"
        data["enable"] = enable
        data["interval"] = interval
        return self.resultdata(data)

    def SendSEI(self, seiMsg: str, length: int):
        data = ApiImpl.getdata()
        data["method"] = "SendSEIMsg"
        data["seiMsg"] = seiMsg
        data["length"] = length
        data["type"] = 0
        return self.resultdata(data)

    def SendSEIStreamType(self, seiMsg: str, length: int, type: int):
        data = ApiImpl.getdata()
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data["method"] = "SendSEIStreamType"
        else:
            data["method"] = "SendSEIMsgWithStreamType"
        data["seiMsg"] = seiMsg
        data["length"] = length
        data["type"] = type
        return self.resultdata(data)

    def EnableEarback(self, enabled: bool, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "EnableEarback"
        data["enabled"] = enabled
        data["volume"] = volume
        return self.resultdata(data)

    def SetEarbackVolume(self, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "SetEarbackVolume"
        data["volume"] = volume
        return self.resultdata(data)

    '''
    file_path   录音文件在本地保存的绝对路径，需要精确到文件名及格式。例如：sdcard/xxx/audio.aac。
    sample_rate 录音采样率（Hz），可以设为 16000、32000（默认）、44100 或 48000
    quality     录音音质，只在 AAC 格式下有效
    '''

    def StartAudioRecording(self, file_path: str, sample_rate: int, quality: int):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioRecording"
        if self.platform == config.MAC:
            data["path"] = file_path
            data["file_path"] = file_path
        else:
            data["file_path"] = file_path
        data["sample_rate"] = sample_rate
        data["quality"] = quality
        return self.resultdata(data)

    '''
    file_path   录音文件在本地保存的绝对路径，需要精确到文件名及格式。例如：sdcard/xxx/audio.aac。
    sample_rate 录音采样率（Hz），可以设为 16000、32000（默认）、44100 或 48000
    quality     录音音质，只在 AAC 格式下有效
    position MIXED_RECORDING_AND_PLAYBACK（默认）0：录制房间内所有成员混流后的音频数据。
                RECORDING 1：仅录制本地用户发布的音频流。
                PLAYBACK 2：仅录制所有远端用户混流后的音频数据。
    cycle_time 循环缓存的最大时长跨度。该参数单位为秒，可以设为 0、10、60、360、900，默认值为 0，即实时写文件
    '''

    def StartAudioRecordingWitchConfig(self, file_path: str, sample_rate: int, quality: int = 0, position: int = 0,
                                       cycle_time: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioRecordingWithConfig"
        data["path"] = file_path
        data["sample_rate"] = sample_rate
        data["quality"] = quality
        data["position"] = position
        data["cycle_time"] = cycle_time
        return self.resultdata(data)

    def StopAudioRecording(self):
        data = ApiImpl.getdata()
        data["method"] = "StopAudioRecording"
        return self.resultdata(data)

    def AddLiveStreamTask(self, task_id: str, stream_url: str, uid: str, extraInfo="", audioBitreate=65,
                          singlePassThrough=False, sampleRate=2, channels=2, codec=0, zOrder=0):
        data = ApiImpl.getdata()
        data["method"] = "AddLiveStreamTask"
        data["task_id"] = task_id
        data["task_stream_url"] = stream_url
        if self.platform == config.LINUX:
            data["task_id"] = str(task_id)
            data["uid"] = str(uid)
        else:
            data["task_id"] = task_id
            data["uid"] = uid
        data["extra_info"] = extraInfo
        data["audio_bitrate"] = audioBitreate
        data["single_video_passthrough"] = singlePassThrough
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["codec"] = codec
        data["z_order"] = zOrder
        return self.resultdata(data)

    def UpdateLiveStreamTask(self, task_id: str, stream_url: str, uid: str, extraInfo=""):
        data = ApiImpl.getdata()
        data["method"] = "UpdateLiveStreamTask"
        data["task_id"] = task_id
        data["task_stream_url"] = stream_url
        data["uid"] = uid
        data["extra_info"] = extraInfo
        return self.resultdata(data)

    def RemoveLiveStreamTask(self, task_id: str, ):
        data = ApiImpl.getdata()
        data["task_id"] = task_id
        data["method"] = "RemoveLiveStreamTask"
        return self.resultdata(data)

    def StartPushStreaming(self, streamingUrl, channelName, token, uid):
        data = ApiImpl.getdata()
        data["streamingUrl"] = streamingUrl
        data["channelName"] = channelName
        data["token"] = token
        data["uid"] = uid
        data["method"] = "StartPushStreaming"
        return self.resultdata(data)

    def StopPushStreaming(self):
        data = ApiImpl.getdata()
        data["method"] = "StopPushStreaming"
        return self.resultdata(data)

    def SetExternalAudioRender(self, enable: bool, sampleRate: int, channels: int):
        data = ApiImpl.getdata()
        data["method"] = "SetExternalAudioRender"
        data["enable"] = enable
        data["sampleRate"] = sampleRate
        data["channels"] = channels
        return self.resultdata(data)

    def SetExternalAudioSource(self, enable: bool, sampleRate: int, channels: int):
        data = ApiImpl.getdata()
        data["method"] = "SetExternalAudioSource"
        data["enable"] = enable
        data["sampleRate"] = sampleRate
        data["channels"] = channels
        return self.resultdata(data)

    def PushExternalAudioFrame(self, audio_type: int, sampleRate: int, channels: int, bytes_per_sample: int,
                               samples_per_channel: int, path: str = "TianKongZhiCheng.pcm", enable: bool = False,
                               disableExternal=False):
        data = ApiImpl.getdata()
        data["method"] = "PushExternalAudioFrame"
        data["type"] = audio_type
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["bytes_per_sample"] = bytes_per_sample
        data["samples_per_channel"] = samples_per_channel
        data["path"] = path
        data["enable"] = enable
        data["disableExternal"] = disableExternal
        return self.resultdata(data)

    def PushExternalVideoAudioFrame(self, audio_type: int, sampleRate: int, channels: int,
                                    audio_path: str = "src_60s.pcm",
                                    video_type=0, video_YType=False, video_path="src_60s.yuv", fps=20, width=640,
                                    height=360, enable: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "PushExternalVideoAudioFrame"
        data["audio_type"] = audio_type
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["audio_path"] = audio_path

        data["video_path"] = video_path
        data["fps"] = fps
        data["width"] = width
        data["height"] = height
        data["video_type"] = video_type
        data["video_YType"] = video_YType

        data["enable"] = enable
        return self.resultdata(data)

    def PullExternalAudioFrame(self, samepleRate: int = 16000, channels: int = 1):
        data = ApiImpl.getdata()
        data["sample_rate"] = samepleRate
        data["channels"] = channels
        data["method"] = "PullExternalAudioFrame"
        return self.resultdata(data)

    def SetExternalVideoSource(self, enable: bool):
        data = ApiImpl.getdata()
        data["enable"] = enable
        data["method"] = "SetExternalVideoSource"
        return self.resultdata(data)

    def push_external_video(self, type1):
        '''向SDK发送外部数据'''
        if self.platform == config.ANDROID:
            file_path = "1280x720_30.mp4"
            self.PushExternalTypeVideoFrame(path=file_path, type1=type1, height=720, width=1280, fps=30)

        elif self.platform == config.IOS:
            file_path = "1280x720_30.yuv"
            self.PushExternalVideoFrame(path=file_path, height=720, width=1280, fps=30)
        else:
            file_path = "1920_1080_30.yuv"
            self.PushExternalTypeVideoFrame(path=file_path, type1=type1, height=1080, width=1920, fps=30)

    def SetExternalTypeVideoSource(self, enable: bool, type1: int):
        data = ApiImpl.getdata()
        data["enable"] = enable
        data["type"] = type1
        data["method"] = "SetExternalTypeVideoSource"
        return self.resultdata(data)

    def SetCaptureDevice(self, device: str, format: int = 0, rotation: int = 0):
        data = ApiImpl.getdata()
        data["device"] = device
        data["format"] = format
        data["rotation"] = rotation
        data["method"] = "SetCaptureDevice"
        return self.resultdata(data)

    def PushExternalVideoFrame(self, path: str = "test2_176_144_15.yuv", format: int = 0, rotation: int = 0, height=144,
                               width=176, fps=30, enable=True, disableExternal=False):
        data = ApiImpl.getdata()
        data["file_path"] = path
        data["format"] = format
        data["rotation"] = rotation
        data["height"] = height
        data["width"] = width
        data["fps"] = fps
        data["enable"] = enable
        data["disableExternal"] = disableExternal
        data["method"] = "PushExternalVideoFrame"
        return self.resultdata(data)

    def PushExternalTypeVideoFrame(self, path: str = "test2_176_144_15.yuv", format: int = 0, rotation: int = 0,
                                   height=144, width=176, fps=30, enable=True, type1=0, disableExternal=False):
        data = ApiImpl.getdata()
        data["file_path"] = path
        data["format"] = format
        data["rotation"] = rotation
        data["height"] = height
        data["width"] = width
        data["fps"] = fps
        data["enable"] = enable
        data["method"] = "PushExternalTypeVideoFrame"
        data["type"] = type1
        data["disableExternal"] = disableExternal
        return self.resultdata(data)

    def SetRecordingAudioFrameParameters(self, channels: int = 2, sample_rate: int = 48000, mode: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SetRecordingAudioFrameParameters"
        data["channels"] = channels
        data["sample_rate"] = sample_rate
        data["mode"] = mode
        return self.resultdata(data)

    def SetPlaybackAudioFrameParameters(self, channels: int = 2, sample_rate: int = 48000, mode: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SetPlaybackAudioFrameParameters"
        data["channels"] = channels
        data["sample_rate"] = sample_rate
        data["mode"] = mode
        return self.resultdata(data)

    def SetMixedAudioFrameParameters(self, channels: int = 2, sample_rate: int = 48000, mode: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SetMixedAudioFrameParameters"
        data["channels"] = channels
        data["sample_rate"] = sample_rate
        data["mode"] = mode
        return self.resultdata(data)

    '''
    开始跨房间媒体流转发
    '''

    def StartChannelMediaRelay(self, src_channel_name: str, src_channel_token: str = "", src_uid: int = 0,
                               dst_channel_names: str = "", dst_channel_token: str = "", dst_uids: str = "10025"):
        data = ApiImpl.getdata()
        data["method"] = "StartChannelMediaRelay"
        if self.platform == config.LINUX:
            data["src_channel_name"] = str(src_channel_name)
            data["src_channel_token"] = str(src_channel_token)
            data["src_uid"] = str(src_uid)
            data["dst_channel_names"] = str(dst_channel_names)
            data["dst_channel_token"] = str(dst_channel_token)
            data["dst_uids"] = str(dst_uids)
        else:
            data["src_channel_name"] = src_channel_name
            data["src_channel_token"] = src_channel_token
            data["src_uid"] = src_uid
            data["dst_channel_names"] = dst_channel_names
            data["dst_channel_token"] = dst_channel_token
            data["dst_uids"] = dst_uids
        return self.resultdata(data)

    '''
    更新媒体流转发的目标房间。
    '''

    def UpdateChannelMediaRelay(self, dst_channel_names: str = "", dst_channel_token: str = "",
                                dst_uids: str = "10025"):
        data = ApiImpl.getdata()
        data["method"] = "UpdateChannelMediaRelay"
        data["dst_channel_names"] = dst_channel_names
        data["dst_channel_token"] = dst_channel_token
        data["dst_uids"] = dst_uids
        return self.resultdata(data)

    '''
    停止跨房间媒体流转发
    '''

    def StopChannelMediaRelay(self):
        data = ApiImpl.getdata()
        data["method"] = "StopChannelMediaRelay"
        return self.resultdata(data)

    def StartAudioDump(self):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioDump"
        return self.resultdata(data)

    def StartAudioDumpWithType(self, dump_type: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "StartAudioDumpWithType"
        '''
        0 仅输出.dump文件（默认）
        1 输出.dump和.wav文件
        2 仅输出.wav文件
        '''
        data["dump_type"] = dump_type
        return self.resultdata(data)

    def StopAudioDump(self):
        data = ApiImpl.getdata()
        data["method"] = "StopAudioDump"
        return self.resultdata(data)

    def UploadSdkInfo(self):
        data = ApiImpl.getdata()
        data["method"] = "UploadSdkInfo"
        return self.resultdata(data)

    def SetClientRole(self, role: int):
        # 0是主播，1是观众
        data = ApiImpl.getdata()
        data["method"] = "SetClientRole"
        data["role"] = role
        return self.resultdata(data)

    def SetSendOnPubType(self, video_sendonpub_type=1):
        data = ApiImpl.getdata()
        data["method"] = "SetPubType"
        data["video_sendonpub_type"] = video_sendonpub_type
        return self.resultdata(data)

    # 设备管理
    def SwitchCamera(self):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SwitchCamera"
        return self.resultdata(data)

    def SwitchCameraWithPosition(self, position: int = 0):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["position"] = position
        data["method"] = "SwitchCameraWithPosition"
        return self.resultdata(data)

    def IsCameraTorchSupported(self):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "IsCameraTorchSupported"
        return self.resultdata(data)

    def SetCameraZoomFactor(self, factor: float):
        # //设置摄像头缩放比例
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SetCameraZoomFactor"
        data["factor"] = factor
        return self.resultdata(data)

    def IsCameraZoomSupported(self):
        # //摄像头是否支持缩放功能
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "IsCameraZoomSupported"
        return self.resultdata(data)

    def IsCameraExposurePositionSupported(self):
        # //检测设备是否支持手动曝光功能。
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "IsCameraExposurePositionSupported"
        return self.resultdata(data)

    def IsCameraFocusSupported(self):
        # //检测设备是否支持手动对焦功能。
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "IsCameraFocusSupported"
        return self.resultdata(data)

    def SetCameraFocusPosition(self, position_x: float, position_y: float):
        # 设置当前摄像头聚焦点位置
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SetCameraFocusPosition"
        data["position_x"] = position_x
        data["position_y"] = position_y
        return self.resultdata(data)

    def SetCameraExposurePosition(self, position_x: float, position_y: float):
        # 设置手动曝光位置
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SetCameraExposurePosition"
        data["position_x"] = position_x
        data["position_y"] = position_y
        return self.resultdata(data)

    def SetCameraTorchOn(self, on: bool):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "SetCameraTorchOn"
        data["on"] = on
        return self.resultdata(data)

    def IsCameraTorchOn(self):
        self.checkPlatform(config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "IsCameraTorchOn"
        return self.resultdata(data)

    def GetCameraMaxZoom(self):
        # 获取摄像头支持的最大缩放比例
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "GetCameraMaxZoom"
        return self.resultdata(data)

    def CheckPermission(self):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "CheckPermission"
        return self.resultdata(data)

    def SetPlayoutDeviceMute(self, muted: bool):
        data = ApiImpl.getdata()
        data["method"] = "SetPlayoutDeviceMute"
        data["muted"] = muted
        return self.resultdata(data)

    def GetPlayoutDeviceMute(self):
        data = ApiImpl.getdata()
        data["method"] = "GetPlayoutDeviceMute"
        return self.resultdata(data)

    def GetPlayoutDeviceVolume(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "GetPlayoutDeviceVolume"
            return self.resultdata(data)

    def SetPlayoutDeviceVolume(self, volume: int = 100):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "SetPlayoutDeviceVolume"
            data["volume"] = volume
            return self.resultdata(data)

    def SetRecordDeviceMute(self, muted: bool):
        data = ApiImpl.getdata()
        data["method"] = "SetRecordDeviceMute"
        data["muted"] = muted
        return self.resultdata(data)

    def SetRecordDeviceVolume(self, volume: int):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "SetRecordDeviceVolume"
            data["volume"] = volume
            return self.resultdata(data)

    def GetRecordDeviceVolume(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "GetRecordDeviceVolume"
            return self.resultdata(data)

    def SetPlayoutDeviceVolume(self, volume: int):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "SetPlayoutDeviceVolume"
            data["volume"] = volume
            return self.resultdata(data)

    def GetPlayoutDeviceVolume(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "GetPlayoutDeviceVolume"
            return self.resultdata(data)

    def EnumerateCaptureDevices(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC or self.platform == config.LINUX:
            data = ApiImpl.getdata()
            data["method"] = "EnumerateCaptureDevices"
            return self.resultdata(data)

    def EnumerateRecordDevices(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "EnumerateRecordDevices"
            return self.resultdata(data)

    def SetLocalPublishFallbackOption(self, fallback_option: int = 0):
        data = ApiImpl.getdata()
        data["fallback_option"] = fallback_option
        data["method"] = "SetLocalPublishFallbackOption"
        return self.resultdata(data)

    def SetRemoteSubscribeFallbackOption(self, fallback_option: int = 0):
        data = ApiImpl.getdata()
        data["fallback_option"] = fallback_option
        data["method"] = "SetRemoteSubscribeFallbackOption"
        return self.resultdata(data)

    def SetLocalMediaPriority(self, priority: int = 0, preemptive: bool = False):
        data = ApiImpl.getdata()
        data["priority"] = priority
        data["preemptive"] = preemptive
        data["method"] = "SetLocalMediaPriority"
        return self.resultdata(data)

    def GetDevice(self):
        if self.platform == config.WINDOWS or self.platform == config.MAC or self.platform == config.LINUX:
            data = ApiImpl.getdata()
            data["method"] = "GetDevice"
            return self.resultdata(data)

    def SetupTypeVideoDevice(self, index=0, type1=0):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "SetupTypeVideoDevice"
            data["type"] = type1
            data["index"] = index
            return self.resultdata(data)

    def GetTypeDevice(self, type1=0):
        if self.platform == config.WINDOWS or self.platform == config.MAC:
            data = ApiImpl.getdata()
            data["method"] = "GetTypeDevice"
            data["type"] = type1
            return self.resultdata(data)

    def GetRecordDeviceMute(self):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "GetRecordDeviceMute"
        return self.resultdata(data)

    def Version(self):
        self.checkPlatform(config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "Version"
        return self.resultdata(data)

    def SetupLocalSubStreamVideoCanvas(self, scalingMode: int, mirrorMode=0, setBgColor: bool = False,
                                       backgroundColor: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SetupLocalSubStreamVideoCanvas"
        data["scalingMode"] = scalingMode
        data["mirrorMode"] = mirrorMode
        if setBgColor:
            data["backgroundColor"] = backgroundColor
        return self.resultdata(data)

    def SetupRemoteSubStreamVideoCanvas(self, scalingMode: int, uid: int, mirrorMode=0, setBgColor: bool = False,
                                        backgroundColor: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SetupRemoteSubStreamVideoCanvas"
        data["scalingMode"] = scalingMode
        data["uid"] = uid
        data["mirrorMode"] = mirrorMode
        if setBgColor:
            data["backgroundColor"] = backgroundColor
        return self.resultdata(data)

    '''
    本地视频画面截图。 调用 takeLocalSnapshot 截取本地主流或本地辅流的视频画面，并通过 NERtcTakeSnapshotCallback 的 onTakeSnapshotResult 回调返回截图画面的数据。
    '''

    def TakeLocalSnapshot(self, streamType: int, uid=0, time=TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)):
        '''
        本地主流截图，需要在 startVideoPreview 或者 enableLocalVideo 并 joinChannel 成功之后调用。
        本地辅流截图，需要在 joinChannel 并 startScreenCapture 之后调用。
        streamType  截图的视频流类型。支持设置为主流或辅流。
        '''
        data = ApiImpl.getdata()
        data["method"] = "TakeLocalSnapshot"
        data["streamType"] = streamType
        data["uid"] = uid
        data["timestamp"] = time
        return self.resultdata(data)

    def TakeLocalCanvasSnapshot(self, streamType: int, uid=0, time=TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)):
        '''
        本地主流截图，需要在 startVideoPreview 或者 enableLocalVideo 并 joinChannel 成功之后调用。
        本地辅流截图，需要在 joinChannel 并 startScreenCapture 之后调用。
        streamType  截图的视频流类型。支持设置为主流或辅流。
        '''
        data = ApiImpl.getdata()
        data["method"] = "TakeLocalCanvasSnapshot"
        data["streamType"] = streamType
        data["uid"] = uid
        data["timestamp"] = time
        return self.resultdata(data)

    def TakeRemoteCanvasSnapshot(self, streamType: int, uid: int,
                           time=TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)):
        '''
        uid 远端用户 ID。
        streamType  截图的视频流类型。支持设置为主流或辅流。
        '''
        data = ApiImpl.getdata()
        data["method"] = "TakeRemoteCanvasSnapshot"
        data["streamType"] = streamType
        data["uid"] = uid
        data["timestamp"] = time
        return self.resultdata(data)

    '''
    远端视频画面截图。 调用 takeRemoteSnapshot 截取指定 uid 远端主流和远端辅流的视频画面，并通过 NERtcTakeSnapshotCallback 的 onTakeSnapshotResult 回调返回截图画面的数据。
    '''

    def TakeRemoteSnapshot(self, streamType: int, uid: int,
                           time=TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)):
        '''
        uid 远端用户 ID。
        streamType  截图的视频流类型。支持设置为主流或辅流。
        '''
        data = ApiImpl.getdata()
        data["method"] = "TakeRemoteSnapshot"
        data["streamType"] = streamType
        data["uid"] = uid
        data["timestamp"] = time
        return self.resultdata(data)

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
                                       loop: bool = True):

        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetLocalCanvasWatermarkConfigs"
            data["streamType"] = streamType
            data["watermark"] = watermark
            data["textOn"] = textOn
            data["timeStampOn"] = timeStampOn
            data["imageOn"] = imageOn
            data["fontColor"] = fontColor
            data["fontSize"] = fontSize
            data["offsetX"] = offsetX
            data["offsetY"] = offsetY
            data["wmColor"] = wmColor
            data["wmHeight"] = wmHeight
            data["wmWidth"] = wmWidth
            data["imageUrl"] = imageUrl
            data["timestamp_fontColor"] = timestamp_fontColor
            data["timestamp_fontSize"] = timestamp_fontSize
            data["timestamp_offsetX"] = timestamp_offsetX
            data["timestamp_offsetY"] = timestamp_offsetY
            data["timestamp_wmColor"] = timestamp_wmColor
            data["timestamp_wmWidth"] = timestamp_wmWidth
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["imageWidth"] = imageWidth
            data["imageHeight"] = imageHeight
            data["image_offsetX"] = imageOffsetX
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["image_offsetY"] = imageOffsetY
            data["fps"] = fps
            data["loop"] = loop

            return self.resultdata(data)

    def SetRemoteCanvasWatermarkConfigs(self, watermark: str = "normal", streamType: int = 0,
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
                                        loop: bool = True, uid: int = 0):

        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SetRemoteCanvasWatermarkConfigs"
            data["watermark"] = watermark
            data["streamType"] = streamType
            data["textOn"] = textOn
            data["timeStampOn"] = timeStampOn
            data["imageOn"] = imageOn
            data["fontColor"] = fontColor
            data["fontSize"] = fontSize
            data["offsetX"] = offsetX
            data["offsetY"] = offsetY
            data["wmColor"] = wmColor
            data["wmHeight"] = wmHeight
            data["wmWidth"] = wmWidth
            data["imageUrl"] = imageUrl
            data["timestamp_fontColor"] = timestamp_fontColor
            data["timestamp_fontSize"] = timestamp_fontSize
            data["timestamp_offsetX"] = timestamp_offsetX
            data["timestamp_offsetY"] = timestamp_offsetY
            data["timestamp_wmColor"] = timestamp_wmColor
            data["timestamp_wmWidth"] = timestamp_wmWidth
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["imageWidth"] = imageWidth
            data["imageHeight"] = imageHeight
            data["image_offsetX"] = imageOffsetX
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["image_offsetY"] = imageOffsetY
            data["fps"] = fps
            data["loop"] = loop
            data["uid"] = uid
            return self.resultdata(data)

    def SetEngineDelegate(self):
        if self.platform == config.IOS:
            data = ApiImpl.getdata()
            data["method"] = "SetEngineDelegate"
            return self.resultdata(data)

    def StartLastmileProbeTest(self, probeUplink: bool = True, probeDownlink: bool = True,
                               expectedUplinkBitratebps: int = 200000,
                               expectedDownlinkBitratebps: int = 200000):
        data = ApiImpl.getdata()
        data["probeUplink"] = probeUplink
        data["probeDownlink"] = probeDownlink
        data["expectedUplinkBitratebps"] = expectedUplinkBitratebps
        data["expectedDownlinkBitratebps"] = expectedDownlinkBitratebps
        data["method"] = "StartLastmileProbeTest"
        return self.resultdata(data)

    def StopLastmileProbeTest(self):
        data = ApiImpl.getdata()
        data["method"] = "StopLastmileProbeTest"
        return self.resultdata(data)

    def SetAudioSubscribeOnlyBy(self, uid_list: str):
        data = ApiImpl.getdata()
        data["method"] = "SetAudioSubscribeOnlyBy"
        data["uids"] = uid_list
        return self.resultdata(data)

    '''
    开启或关闭媒体流加密。
    请在加入房间前调用该方法，加入房间后无法修改加密模式与密钥。用户离开房间后，SDK 会自动关闭加密。如需重新开启加密，需要在用户再次加入房间前调用此方法。
    '''

    def EnableEncryption(self, enable: bool = False, mode: int = 0, key: str = "afh8465478777777777464654564s"):
        data = ApiImpl.getdata()
        '''
        enable  是否开启媒体流加密。
        mode 媒体流加密模式, 媒体流加密模式 使用默认值0， kNERtcGMCryptoSM4ECB 128 位 SM4 加密，ECB 模式
        key 媒体流加密密钥
        '''
        data["enable"] = enable
        data["mode"] = mode
        data["key"] = key
        data["method"] = "EnableEncryption"
        return self.resultdata(data)

    '''
    开启或关闭虚拟背景
    '''

    def EnableVirtualBackground(self, enable: bool = False, path: str = "", bg_sourcetype: int = 0,
                                color: str = "0xffffff", degree: int = 3):
        data = ApiImpl.getdata()
        '''
        enable  是否开启虚拟背景。
        path 自定义背景图片的本地绝对路径。支持 PNG 和 JPG 格式。
        bg_sourcetype 自定义背景图片的类型：kNERtcBackgroundColor 1：（默认）背景图像为纯色。
                                        kNERtcBackgroundImage 2：背景图像只支持 PNG 或 JPG 格式的文件。
                                        kNERtcBackgroundBlur 3：背景图虚化。
        degree: 1 low  2 mid 3 high
        '''
        data["enable"] = enable
        data["path"] = path
        data["bg_sourcetype"] = bg_sourcetype
        data["color"] = color
        data["degree"] = degree
        data["method"] = "EnableVirtualBackground"
        return self.resultdata(data)

    def SetVirtualBackground(self, value1=15):
        update_data = {
            "engine.video.pre_process_type": value1
        }
        para_dict = HttpUtils.get_demo_config(config.AppKey, config.Video)

        para_dict = HttpUtils.update_demo_config(self.platform, para_dict, self.cpu, update_data)
        HttpUtils.post_demo_config(config.AppKey, data1=para_dict, key=config.Video)

    def SetRemoteHighPriorityAudioStream(self, enable: bool = False, uid: int = 0, cname: str = ""):
        data = ApiImpl.getdata()
        '''
        设置远端用户音频流为高优先级。 支持在音频自动订阅的情况下，设置某一个远端用户的音频为最高优先级，可以优先听到该用户的音频。
        '''
        data["enable"] = enable
        data["uid"] = uid
        data["cname"] = cname
        data["method"] = "SetRemoteHighPriorityAudioStream"
        return self.resultdata(data)

    def SetCloudProxy(self, proxyType: int = 0):
        '''0关闭，1开启'''
        data = ApiImpl.getdata()
        '''
        开启并设置云代理服务
        '''
        data["proxyType"] = proxyType
        data["method"] = "SetCloudProxy"
        return self.resultdata(data)

    '''
    编码水印
    '''

    def SetLocalVideoWatermarkConfigs(self, enable: bool = True, mode: int = 1,
                                      wm_alpha: float = 0.8, streamType: int = 0,
                                      wm_width: int = 100, wm_height: int = 100,
                                      fontColor: str = "0x000000FF", fontSize: int = 10,
                                      offsetX: int = 0, offsetY: int = 0,
                                      content: str = "Test", fontPath="test_watermark_text_context",
                                      wmColor: str = "0x00888888",
                                      imageUrl: str = "water1.png", fps: int = 5,
                                      loop: bool = True):
        data = ApiImpl.getdata()
        data["method"] = "SetLocalVideoWatermarkConfigs"
        data["stream_type"] = streamType
        data["enable"] = enable
        '''
        mode:  图片0   文字1  时间戳 2
        '''
        data["mode"] = mode
        data["wm_alpha"] = wm_alpha
        data["wm_width"] = wm_width
        data["wm_height"] = wm_height
        data["fontColor"] = fontColor
        data["fontSize"] = fontSize
        data["fontPath"] = fontPath
        data["offset_x"] = offsetX
        data["offset_y"] = offsetY
        data["content"] = content
        data["wm_color"] = wmColor
        data["image_paths"] = imageUrl
        data["fps"] = fps
        data["loop"] = loop

        return self.resultdata(data)

    def SetLocalVoiceReverbPara(self, proxyType: int = 0):
        data = ApiImpl.getdata()
        data["proxyType"] = proxyType
        data["method"] = "SetLocalVoiceReverbPara"
        return self.resultdata(data)

    '''
    发布/停止本地音频
    '''

    def EnableMediaPub(self, enable: bool = False, media_type: int = 0):
        data = ApiImpl.getdata()
        data["media_type"] = media_type
        data["enable"] = enable
        data["method"] = "EnableMediaPub"
        return self.resultdata(data)

    '''
    是否开启精准对齐功能
    '''

    def SetStreamAlignmentProperty(self, ):
        data = ApiImpl.getdata()
        data["method"] = "SetStreamAlignmentProperty"
        return self.resultdata(data)

    '''
    获取本地系统时间与服务端时间差值 
    '''

    def GetNtpTimeOffset(self, ):
        data = ApiImpl.getdata()
        data["method"] = "GetNtpTimeOffset"
        return self.resultdata(data)

    def SetScreenCaptureMouseCursor(self, enable: bool = False):
        data = ApiImpl.getdata()
        data["capture_cursor"] = enable
        data["method"] = "SetScreenCaptureMouseCursor"
        return self.resultdata(data)

    '''
    是否启用视频图像畸变矫正
    开启该功能时，根据合适的参数，可以通过算法把这个形变进行复原。
    矫正参数生效后，本地画面和对端看到的画面，均会是矫正以后的画面
    '''

    def EnableVideoCorrection(self, enable: bool = False):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["enable"] = enable
        data["method"] = "EnableVideoCorrection"
        return self.resultdata(data)

    '''
    设置视频图像矫正参数
    每个坐标点的 x 和 y 的取值范围均为 0 ~ 1 的浮点数
    enableMirror, width, height 参数只有在使用了外部视频渲染功能时才需要传入
    '''

    def SetVideoCorrectionConfig(self, enableMirror: bool = True, width: int = 0, height: int = 0,
                                 enable: bool = True,
                                 left_top_x: int = 0, left_top_y: int = 0,
                                 right_top_x: int = 0, right_top_y: int = 0,
                                 left_bottom_x: int = 0, left_bottom_y: int = 0,
                                 right_bottom_x: int = 0, right_bottom_y: int = 0):
        self.checkPlatform(config.IOS, config.ANDROID)
        data = ApiImpl.getdata()
        data["enableMirror"] = enableMirror
        data["width"] = width
        data["height"] = height
        data["left_top_x"] = left_top_x
        data["left_top_y"] = left_top_y
        data["right_top_x"] = right_top_x
        data["right_top_y"] = right_top_y
        data["left_bottom_x"] = left_bottom_x
        data["left_bottom_y"] = left_bottom_y
        data["right_bottom_x"] = right_bottom_x
        data["right_bottom_y"] = right_bottom_y
        data["enable"] = enable
        data["method"] = "SetVideoCorrectionConfig"
        return self.resultdata(data)

    '''
    开启美颜
    '''

    def StartBeauty(self, file_path: str = ''):
        data = ApiImpl.getdata()
        # data["enable"] = enable
        data["method"] = "StartBeauty"
        data["filePath"] = file_path
        return self.resultdata(data)

    '''
    关闭美颜
    '''

    def StopBeauty(self):
        data = ApiImpl.getdata()
        data["method"] = "StopBeauty"
        return self.resultdata(data)

    '''
    开启/暂停美颜
    '''

    def EnableBeauty(self, enable: bool = False):
        data = ApiImpl.getdata()
        data["enable"] = enable
        data["method"] = "EnableBeauty"
        return self.resultdata(data)

    '''
    设置美颜类型和强度
    '''

    def SetBeautyEffect(self, beautytype: int = 0, level: float = 0):
        data = ApiImpl.getdata()
        data["beautyType"] = beautytype
        data["level"] = level
        data["method"] = "SetBeautyEffect"
        return self.resultdata(data)

    '''
    导入美颜资源或模型
    '''

    def AddTempleteWithPath(self, path, name):
        data = ApiImpl.getdata()
        data["path"] = path
        data["name"] = name
        data["method"] = "AddBeautyTemplete"
        return self.resultdata(data)

    '''
    添加滤镜效果
    '''

    def AddBeautyFilter(self, position):
        data = ApiImpl.getdata()
        data["position"] = position
        data["method"] = "AddBeautyFilter"
        return self.resultdata(data)

    '''
    取消滤镜效果
    '''

    def RemoveBeautyFilter(self):
        data = ApiImpl.getdata()
        data["method"] = "RemoveBeautyFilter"
        return self.resultdata(data)

    '''
    添加贴纸效果
    '''

    def AddBeautySticker(self, sticker, position):
        data = ApiImpl.getdata()
        data["sticker"] = sticker
        data["position"] = position
        data["method"] = "AddBeautySticker"
        return self.resultdata(data)

    '''
    取消贴纸效果
    '''

    def RemoveBeautySticker(self):
        data = ApiImpl.getdata()
        data["method"] = "RemoveBeautySticker"
        return self.resultdata(data)

    '''
     添加美妆效果
     '''

    def AddBeautyMakeup(self, sticker: str = "makeup", position: int = 0):
        data = ApiImpl.getdata()
        data["sticker"] = sticker
        data["position"] = position
        data["method"] = "AddBeautyMakeup"
        return self.resultdata(data)

    '''
    取消美妆效果
    '''

    def RemoveBeautyMakeup(self):
        data = ApiImpl.getdata()
        data["method"] = "RemoveBeautyMakeup"
        return self.resultdata(data)

    '''    
    上传音频，图片，视频等压缩文件
    '''

    def UploadAssets(self, url: str = "", path: str = "", cid: str = "", uid: str = "", zip_name: str = ""):
        data = ApiImpl.getdata()
        data["url"] = url
        data["path"] = path
        data["cid"] = cid
        data["uid"] = uid
        data["appkey"] = config.AppKey
        data["zip_name"] = zip_name
        data["method"] = "UploadAssets"
        return self.resultdata(data)

    '''
    本地音频，图片等生成压缩文件，文件名可传入
    '''

    def ZipAssets(self, path: str = "", file_names: str = "", zip_name: str = ""):
        data = ApiImpl.getdata()
        data["path"] = path
        data["file_names"] = file_names
        data["zip_name"] = zip_name
        data["appkey"] = config.AppKey
        data["method"] = "ZipAssets"
        return self.resultdata(data)

    def ZipCanvasAssets(self, path: str = "", file_names: str = "", zip_name: str = ""):
        data = ApiImpl.getdata()
        data["path"] = path
        data["file_names"] = file_names
        data["zip_name"] = zip_name
        data["appkey"] = config.AppKey
        data["method"] = "ZipCanvasAssets"
        return self.resultdata(data)

    def ZipFolder(self, path: str = "", folder_name: str = "", zip_name: str = ""):
        data = ApiImpl.getdata()
        data["path"] = path
        data["folder_name"] = folder_name
        data["zip_name"] = zip_name
        data["method"] = "ZipFolder"
        return self.resultdata(data)

        '''
        打开视频预览
        '''

    def handlePreviewUI(self, openUI=True):
        if self.platform == config.IOS:
            data = ApiImpl.getdata()
            data["open"] = openUI
            data["method"] = "handlePreviewUI"
            return self.resultdata(data)

    '''
    推送外部音频主流编码帧
    主动将音频编码帧数据用 NERtcAudioEncodedFrame 类封装后传递给 SDK
    '''

    def PushExternalAudioEncodedFrame(self, sampleRate: int, channels: int, path: str = "TianKongZhiCheng.pcm",
                                      enable: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "PushExternalAudioEncodedFrame"
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["path"] = path
        data["enable"] = enable
        return self.resultdata(data)

    '''
    推送外部音频辅流编码帧
    将音频编码帧数据用 NERtcAudioEncodedFrame 类封装后传递给 SDK
    '''

    def PushExternalSubStreamAudioEncodedFrame(self, sampleRate: int, channels: int, path: str = "TianKongZhiCheng.pcm",
                                               enable: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "PushExternalSubStreamAudioEncodedFrame"
        data["sample_rate"] = sampleRate
        data["channels"] = channels
        data["path"] = path
        data["enable"] = enable
        return self.resultdata(data)

    '''
    发送外部视频编码帧
    安卓端path 外部视频读取目前在  Android/data/com.netease.rtcdemo/files目录下，或者在/sdcard目录下
    streamType 0 是主流， 1是辅流
    yuv文件的 height, width必须传正确的视频长宽
    videoType 代表yuv的格式，0是I420. 1代表NV21
    yuv有很多编码格式，其中yuv420就是一种，而nv21又是yuv420的一种。并且nv21是针对android设备的视频编码
    I420也是YUV420编码格式的一种，由于android手机厂商的原因，摄像头采集到的数据永远都是经过NV21编码的数据，但是对于这种数据不能够显示在苹果或windows平台，
    那么需要对这个编码格式的数据需要重新编码，其中I420这种编码格式，所有的厂商都是适配的。
    '''

    def PushExternalVideoEncodedFrame(self, path: str = "test2_176_144_15.yuv", streamType: int = 0,
                                      height=144, width=176, fps=30, enable=True, videoType: int = 0):
        data = ApiImpl.getdata()
        data["file_path"] = path
        data["height"] = height
        data["width"] = width
        data["fps"] = fps
        data["enable"] = enable
        data["app_key"] = config.AppKey
        data["video_type"] = videoType
        data["stream_type"] = streamType
        data["method"] = "PushExternalVideoEncodedFrame"
        return self.resultdata(data)

    '''
    关闭SDK 视频解码 ， 实际是通过setParameters 设
    '''

    def DisableVideoDecoder(self, enable=False):
        data = ApiImpl.getdata()
        data["enable"] = enable
        data["method"] = "DisableVideoDecoder"
        return self.resultdata(data)

    '''
    注册解码前媒体数据观测器
    '''

    def SetPreDecodeObserver(self, ):
        data = ApiImpl.getdata()
        data["app_key"] = config.AppKey
        data["method"] = "SetPreDecodeObserver"
        return self.resultdata(data)

    '''
    设置视频编码qos信息监听器
    '''

    def SetVideoEncoderQosObserver(self, ):
        data = ApiImpl.getdata()
        data["app_key"] = config.AppKey
        data["method"] = "SetVideoEncoderQosObserver"
        return self.resultdata(data)

        '''多房间方法'''

    def CreateChannel(self, channelName: str):
        # if self.platform != config.MAC:
        data = ApiImpl.getdata()
        data["method"] = "CreateChannel"
        if self.platform == config.WINDOWS:
            data["channel_name"] = channelName
        else:
            data["channelName"] = channelName
        return self.resultdata(data)

    def GetSubRoomChannelList(self):
        data = ApiImpl.getdata()
        data["method"] = "GetSubRoomChannelList"
        return self.resultdata(data)

    def GetChannelName(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomGetChannelName"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomJoinChannel(self, channelName: str, uid: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomJoinChannel"
        data["channelName"] = channelName
        data["token"] = ""
        data["uid"] = uid
        return self.resultdata(data)

    def SubRoomLeaveChannel(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomLeaveChannel"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomMuteLocalAudioStream(self, mute: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomMuteLocalAudioStream"
        data["mute"] = mute
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomEnableLocalAudio(self, enable: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomEnableLocalAudio"
        data["enable"] = enable
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetStatsObserver(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetStatsObserver"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetChannelCallback(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetChannelCallback"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomClearProfile(self, channelName: str):
        if self.platform == config.IOS:
            data = ApiImpl.getdata()
            data["method"] = "SubRoomCleanupChannelMediaStatsObserver"
            data["channelName"] = channelName
            return self.resultdata(data)

    def SubRoomMuteLocalVideoStream(self, mute: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomMuteLocalVideoStream"
        data["mute"] = mute
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomMuteLocalTypeVideoStream(self, mute: bool, channelName: str, type1: int):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomMuteLocalTypeVideoStream"
        data["mute"] = mute
        data["channelName"] = channelName
        data["type"] = type1
        return self.resultdata(data)

    def SubRoomEnableLocalVideo(self, enable: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomEnableLocalVideo"
        data["enable"] = enable
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomEnableTypeLocalVideo(self, enable: bool, channelName: str, type1: int):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomEnableTypeLocalVideo"
        data["enable"] = enable
        data["type"] = type1
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomRelease(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomRelease"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomStartScreenCaptureByScreenRect(self, channelName: str, profile=1, bitrate=0, frameRate=5, width=0,
                                              height=0, prefer=0):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomStartScreenCaptureByScreenRect"
        data["profile"] = profile
        data["bitrate"] = bitrate
        data["frameRate"] = frameRate
        data["width"] = width
        data["height"] = height
        data["prefer"] = prefer
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomUpdateScreenCaptureRegion(self, channelName: str, x: int = 0, y: int = 0, width: int = 0,
                                         height: int = 0):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomUpdateScreenCaptureRegion"
        data["x"] = x
        data["y"] = y
        data["width"] = width
        data["height"] = height
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetCaptureProfile(self, channelName: str, profile: int = 0):
        data = ApiImpl.getdata()
        """
                profile1: 0   640*480
                profile1: 1   1280*720
                profile1: 2   1920*1080
                profile1: 3   自定义
                """
        self.checkPlatform(config.WINDOWS)
        data["method"] = "SubRoomSetCaptureProfile"
        data["profile"] = profile
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomStartScreenCaptureByWindowId(self, channelName: str):
        data = ApiImpl.getdata()
        self.checkPlatform(config.WINDOWS)
        data["method"] = "SubRoomStartScreenCaptureByWindowId"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomStopScreenCapture(self, channelName: str):
        data = ApiImpl.getdata()
        self.checkPlatform(config.WINDOWS)
        data["method"] = "SubRoomStopScreenCapture"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomPauseScreenCapture(self, channelName: str):
        data = ApiImpl.getdata()
        self.checkPlatform(config.WINDOWS)
        data["method"] = "SubRoomPauseScreenCapture"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomResumeScreenCapture(self, channelName: str):
        data = ApiImpl.getdata()
        self.checkPlatform(config.WINDOWS)
        data["method"] = "SubRoomResumeScreenCapture"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetupLocalVideoCanvas(self, scalingMode: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetupLocalVideoCanvas"
        data["scalingMode"] = scalingMode
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetupRemoteVideoCanvas(self, uid: str, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetupRemoteVideoCanvas"
        data["userId"] = uid
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetupLocalSubStreamVideoCanvas(self, scalingMode: int, channelName: str):
        if self.platform != config.ANDROID:
            data = ApiImpl.getdata()
            data["method"] = "SubRoomSetupLocalSubStreamVideoCanvas"
            data["scalingMode"] = scalingMode
            data["channelName"] = channelName
            return self.resultdata(data)

    def SubRoomSetLocalRenderMode(self, scalingMode: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetLocalRenderMode"
        data["scalingMode"] = scalingMode
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetRemoteRenderMode(self, scalingMode: int, uid: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetRemoteRenderMode"
        data["scalingMode"] = scalingMode
        data["uid"] = uid
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetupRemoteSubStreamVideoCanvas(self, scalingMode: int, uid: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetupRemoteSubStreamVideoCanvas"
        data["scalingMode"] = scalingMode
        data["uid"] = uid
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetLocalVideoMirrorMode(self, mirror_mode: int, channelName: str):
        self.checkPlatform(config.WINDOWS, config.MAC)
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetLocalVideoMirrorMode"
        data["mirror_mode"] = mirror_mode
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomEnableDualStreamMode(self, enable: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomEnableDualStreamMode"
        data["enable"] = enable
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetClientRole(self, role: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetClientRole"
        data["role"] = role
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomGetConnectionState(self, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomGetConnectionState"
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetLocalVideoConfig(self, channelName: str, maxProfile=0, cropMode=0, frameRate=0, minFrameRate=0,
                                   maxBitrate=0, minBitrate=0, degradationPreference=0, frontCamera=False,
                                   colorFormat=0, mirrorMode=0, width=0, height=0, orientationMode=0):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetLocalVideoConfig"
        data["maxProfile"] = maxProfile
        data["cropMode"] = cropMode
        data["frameRate"] = frameRate
        data["minFrameRate"] = minFrameRate
        data["maxBitrate"] = maxBitrate
        data["minBitrate"] = minBitrate
        data["degradationPreference"] = degradationPreference
        data["frontCamera"] = frontCamera
        data["colorFormat"] = colorFormat
        data["mirrorMode"] = mirrorMode
        data["orientationMode"] = orientationMode
        data["channelName"] = channelName
        data["width"] = width
        data["height"] = height
        return self.resultdata(data)

    def SubRoomSetCameraCaptureConfig(self, channelName: str, preference: int, height: int, width: int):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetCameraCaptureConfig"
        data["channelName"] = channelName
        """
        preference = 0 CAPTURE_PREFERENCE_DEFAULT （默认）优先保证设备性能,
        参考用户在 setLocalVideoConfig 中设置编码器的分辨率和帧率，选择最接近的摄像头输出参数。在这种情况下，预览质量接近于编码器的输出质量。

        preference = 1 CAPTURE_PREFERENCE_MANUAL 采用用户自定义设置的摄像头输出参数
        此时用户可以通过 width 和 height 设置本地摄像头采集的视频宽高

        preference = 2 CAPTURE_PREFERENCE_OUTPUT_QUALITY 优先保证视频预览质量。
        SDK 自动设置画质较高的摄像头输出参数，提高预览画面质量。此时会消耗更多的 CPU 及内存做视频前处理。
        """

        data["preference"] = preference
        data["width"] = width
        data["height"] = height
        return self.resultdata(data)

    def SubRoomSetTypeCameraCaptureConfig(self, channelName: str, preference: int, height: int, width: int, type1: int):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSetTypeCameraCaptureConfig"
        data["channelName"] = channelName
        """
        preference = 0 CAPTURE_PREFERENCE_DEFAULT （默认）优先保证设备性能,
        参考用户在 setLocalVideoConfig 中设置编码器的分辨率和帧率，选择最接近的摄像头输出参数。在这种情况下，预览质量接近于编码器的输出质量。

        preference = 1 CAPTURE_PREFERENCE_MANUAL 采用用户自定义设置的摄像头输出参数
        此时用户可以通过 width 和 height 设置本地摄像头采集的视频宽高

        preference = 2 CAPTURE_PREFERENCE_OUTPUT_QUALITY 优先保证视频预览质量。
        SDK 自动设置画质较高的摄像头输出参数，提高预览画面质量。此时会消耗更多的 CPU 及内存做视频前处理。
        """

        data["preference"] = preference
        data["width"] = width
        data["height"] = height
        data["type"] = type1
        return self.resultdata(data)

    def SubRoomSubscribeRemoteAudio(self, uid: int, subscribe: bool, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSubscribeRemoteAudioStream"
        data["uid"] = uid
        data["subscribe"] = subscribe
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSubscribeRemoteVideo(self, uid: int, subscribe: bool, streamType: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSubscribeRemoteVideoStream"
        data["uid"] = uid
        data["subscribe"] = subscribe
        data["streamType"] = streamType
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomTakeLocalSnapshot(self, streamType: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomTakeLocalSnapshot"
        data["streamType"] = streamType
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSendSEI(self, seiMsg: str, length: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSendSEIMsg"
        data["seiMsg"] = seiMsg
        data["length"] = length
        data["type"] = 0
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSendSEIStream(self, seiMsg: str, length: int, type: int, channelName: str):
        data = ApiImpl.getdata()
        data["method"] = "SubRoomSendSEIMsgStream"
        data["seiMsg"] = seiMsg
        data["length"] = length
        data["type"] = type
        data["channelName"] = channelName
        return self.resultdata(data)

    def SubRoomSetLocalCanvasWatermarkConfigs(self, channelName: str, watermark: str = "normal", streamType: int = 0,
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
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SubRoomSetLocalCanvasWatermarkConfigs"
            data["streamType"] = streamType
            data["watermark"] = watermark
            data["channelName"] = channelName
            data["textOn"] = textOn
            data["timeStampOn"] = timeStampOn
            data["imageOn"] = imageOn
            data["fontColor"] = fontColor
            data["fontSize"] = fontSize
            data["offsetX"] = offsetX
            data["offsetY"] = offsetY
            data["wmColor"] = wmColor
            data["wmHeight"] = wmHeight
            data["wmWidth"] = wmWidth
            data["imageUrl"] = imageUrl
            data["timestamp_fontColor"] = timestamp_fontColor
            data["timestamp_fontSize"] = timestamp_fontSize
            data["timestamp_offsetX"] = timestamp_offsetX
            data["timestamp_offsetY"] = timestamp_offsetY
            data["timestamp_wmColor"] = timestamp_wmColor
            data["timestamp_wmWidth"] = timestamp_wmWidth
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["imageWidth"] = imageWidth
            data["imageHeight"] = imageHeight
            data["image_offsetX"] = imageOffsetX
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["image_offsetY"] = imageOffsetY
            data["fps"] = fps
            data["loop"] = loop
            return self.resultdata(data)

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
        if self.platform == config.WINDOWS:
            data = ApiImpl.getdata()
            data["method"] = "SubRoomSetRemoteCanvasWatermarkConfigs"
            data["streamType"] = streamType
            data["watermark"] = watermark
            data["channelName"] = channelName
            data["textOn"] = textOn
            data["timeStampOn"] = timeStampOn
            data["imageOn"] = imageOn
            data["fontColor"] = fontColor
            data["fontSize"] = fontSize
            data["offsetX"] = offsetX
            data["offsetY"] = offsetY
            data["wmColor"] = wmColor
            data["wmHeight"] = wmHeight
            data["wmWidth"] = wmWidth
            data["imageUrl"] = imageUrl
            data["timestamp_fontColor"] = timestamp_fontColor
            data["timestamp_fontSize"] = timestamp_fontSize
            data["timestamp_offsetX"] = timestamp_offsetX
            data["timestamp_offsetY"] = timestamp_offsetY
            data["timestamp_wmColor"] = timestamp_wmColor
            data["timestamp_wmWidth"] = timestamp_wmWidth
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["imageWidth"] = imageWidth
            data["imageHeight"] = imageHeight
            data["image_offsetX"] = imageOffsetX
            data["timestamp_wmHeight"] = timestamp_wmHeight
            data["image_offsetY"] = imageOffsetY
            data["fps"] = fps
            data["loop"] = loop
            data["uid"] = uid
            return self.resultdata(data)

    # data channel
    '''
    开关data channel
    '''

    def EnableLocalData(self, enabled: bool):
        data = ApiImpl.getdata()
        data["method"] = "EnableLocalData"
        data["enabled"] = enabled
        return self.resultdata(data)

    def SubscribeRemoteData(self, uid: str, subscribe: bool):
        data = ApiImpl.getdata()
        data["method"] = "SubscribeRemoteData"
        data["uid"] = uid
        data["subscribe"] = subscribe
        return self.resultdata(data)

    def SetAudoSubscribeVideo(self, auto_subscribe_video: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "SetAudoSubscribeVideo"
        data["auto_subscribe_video"] = auto_subscribe_video
        return self.resultdata(data)

    def SetAudoSubscribeData(self, auto_subscribe_data: bool = False):
        data = ApiImpl.getdata()
        data["method"] = "SetAudoSubscribeData"
        data["auto_subscribe_data"] = auto_subscribe_data
        return self.resultdata(data)

    def SendDataWithString(self, content: str, repeatTime: int = 1):
        data = ApiImpl.getdata()
        data["method"] = "SendData"
        data["content"] = content
        data["repeatTime"] = repeatTime
        return self.resultdata(data)

    def SendDataWithFile(self, fileName: str, repeatTime: int = 1):
        data = ApiImpl.getdata()
        data["method"] = "SendData"
        data["fileName"] = fileName
        data["repeatTime"] = repeatTime
        return self.resultdata(data)

    def GetLatestReceiveData(self):
        data = ApiImpl.getdata()
        data["method"] = "GetLatestReceiveData"
        return self.resultdata(data)

    def GetLatestReceiveDataSize(self):
        data = ApiImpl.getdata()
        data["method"] = "GetLatestReceiveDataSize"
        return self.resultdata(data)

    def GetLatestSendDataSize(self):
        data = ApiImpl.getdata()
        data["method"] = "GetLatestSendDataSize"
        return self.resultdata(data)

    def InitPstn(self):
        self.checkPlatform(config.ANDROID, config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "InitPstn"
        return self.resultdata(data)

    def PstnRelease(self):
        self.checkPlatform(config.ANDROID, config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "PstnRelease"
        return self.resultdata(data)

    def DirectCallHangup(self):
        self.checkPlatform(config.ANDROID, config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "DirectCallHangup"
        return self.resultdata(data)

    def DirectCallStartCall(self, app_key: str = config.AppKey,
                            callee: str = "15657132163",
                            channel_name: str = "",
                            uid: str = "0",
                            did_number: str = "01086486717",
                            token: str = "1",
                            trace_id: str = "",
                            is_fail=False):
        self.checkPlatform(config.ANDROID, config.IOS)
        data = ApiImpl.getdata()
        data["app_key"] = app_key
        data["token"] = token
        data["callee"] = callee
        data["channel_name"] = channel_name
        if is_fail:
            data["uid"] = 0
        else:
            data["uid"] = uid
        data["did_number"] = did_number
        data["trace_id"] = trace_id
        data["method"] = "DirectCallStartCall"
        return self.resultdata(data)

    '''
       开关音频共享
    '''

    def EnableLoopbackRecording(self, enable: bool):
        data = ApiImpl.getdata()
        data["method"] = "EnableLoopbackRecording"
        data["enable"] = enable
        return self.resultdata(data)

    '''
    调节音频共享音量
    '''

    def AdjustLoopbackRecordingSignalVolume(self, volume: int):
        data = ApiImpl.getdata()
        data["method"] = "AdjustLoopbackRecordingSignalVolume"
        data["volume"] = volume
        return self.resultdata(data)

    def SetLoudspeakerMode(self, enable: bool):
        '''此接口只支持iOS和Android'''
        data = ApiImpl.getdata()
        data["method"] = "SetLoudspeakerMode"
        data["enable"] = enable
        return self.resultdata(data)

    def GetLoudspeakerMode(self):
        '''此接口只支持iOS和Android'''
        data = ApiImpl.getdata()
        data["method"] = "GetLoudspeakerMode"
        return self.resultdata(data)

    def SetForwardIP(self, ip: str):
        self.checkPlatform(config.IOS)
        data = ApiImpl.getdata()
        data["method"] = "SetForwardIP"
        data["forward_ip"] = ip
        return self.resultdata(data)

    def GetAudioMixingPitch(self):
        self.checkPlatform(config.ANDROID)
        data = ApiImpl.getdata()
        data["method"] = "GetAudioMixingPitch"
        return self.resultdata(data)

    def resultdata(self, data: dict):
        OutputUtils.print(self.info["platform"] + ": " + self.info["userId"])
        OutputUtils.print(data)
        s = SocketClient(self.ip, self.port)
        if self.platform == config.WINDOWS:
            recv_data = s.sender_windows(data)
        else:
            recv_data = s.sender(data)
        s.close()
        OutputUtils.print(
            data["method"] + " call finished at： " + TimeUtils.get_cur_time().strftime(TimeUtils.time_format))
        return recv_data

    def checkPlatform(self, *args):
        if self.platform not in args:
            raise Exception("该方法只适用于: {}".format(args))


if __name__ == '__main__':
    url = config.MAIN_NODE + """/es/getReportData?jobTaskId=%s&method=%s&channel_name=%s""" % ("10589",
                                                                                               "onLocalVideoStats",
                                                                                               "200132")

    data = HttpUtils.get(url)

    OutputUtils.print(data)
