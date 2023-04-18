import config
from netease_test.netease_case1 import NeteaseCase
from api_common.api_common import ApiCommon
from api_common.case_common import CaseCommon
from profile1.ProfileEnum import ProfileEnum
from utils.time_utils import TimeUtils
from numpy import mean
import time
import json


class AudioMediaPubSetting(NeteaseCase):

    def setUp(self, **kwargs):
        self.OutputUtils.print("setup")
        self.task_cases_id = kwargs["task_cases_id"]
        self.api = ApiCommon(kwargs["user_list"])

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235469&view=table
    通话前设置pub开关为false，入会后查看音量回调、音频回调等是否正常 
    '''
    def test_audio_media_pub(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        self.api.EnableLocalAudio(True)
        '''设备0上报采集的音频信息'''
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        '''
        等待一段时间，透明数据2秒上报一次，多收集几组数据求平均来确保数据的准确性
        '''
        time.sleep(config.ReportTime)
        '''
        根据cname ,回调方法名， uid 查询到设备0本地音频上报的信息
        获取到json信息后，计算得到上报的码率，采样率的平均值
        '''
        bit_rate, sent_volume = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("发送码率: " + str(bit_rate))
        self.OutputUtils.print("发送音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("Pub开关设置为False, 期望音量透明数据统计不回调，实际音量有值")

        '''
        此时录制的音频有系统声音，是否有声音的断言判断还是有声音的
        '''
        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235469&view=table
    通话前设置pub开关为false，入会后查看音量提示回调等是否正常 
    '''
    def test_audio_media_pub_volume_indication(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        self.api.EnableLocalAudio(True)

        '''
        开启音量提示
        '''
        self.api.assert_error(self.api.user_list[0].EnableAudioVolumeIndication(True, 1000))
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id, ProfileEnum.onRemoteAudioVolumeIndication)

        self.OutputUtils.print("远端音量提示:" + str(remote_volume_indication))

        if len(remote_volume_indication) > 0:
            speaker_list = list(map(lambda x: int(json.loads(x["_source"]["data"])["uid"]), remote_volume_indication))
            total_volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["total_volume"]), remote_volume_indication))
            self.OutputUtils.print("远端说话者数量:" + str(speaker_list))
            self.OutputUtils.print("混音后的音量:" + str(total_volume_list))
            total_volume = mean(total_volume_list)

            if total_volume > 0:
                raise BaseException("Pub开关设置为False, 期望音量提示是0")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235469&view=table
    通话前设置pub开关为false，入会后查看音频回调等是否正常 
    '''
    def test_audio_media_pub_audio_callback(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        '''
        生成pcm文件的时间戳，文件命名用到
        '''
        registered_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        开启音频回调，回调文件生成规则为回调类型+用户id+声道数+ 采样率+ 时间戳.pcm
        如 Mixed_12320_1_48000_20200814xxx.pcm
        '''
        self.api.user_list[0].SetAudioFrameObserver(uid=self.api.user_list[0].uid, curtime=registered_time)
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        self.api.EnableLocalAudio(True)


        time.sleep(8)
        '''
        获取pcm录制回调的采样率,声道数
        '''
        samepleRate, channels = CaseCommon.get_audio_callback_info(self.task_cases_id, self.api.user_list, ProfileEnum.onRecordFrame)
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))

        self.OutputUtils.print("RecordFrame sample rate, channels : " + str(samepleRate) + str("," + str(channels)))
        self.api.assert_error(self.api.user_list[0].EnableLocalAudio(False))
        '''
        关闭音频回调
        '''
        self.api.user_list[0].SetAudioFrameObserver(uid=self.api.user_list[0].uid, switch=False)
        time.sleep(5)
        '''
        record pcm playback pcm ,mixed pcm 文件压缩上传到服务端, 脚本可根据采样率，声道数，时间戳去服务端找到相应的文件
        服务端调用脚本分析生成的pcm 文件是否有声音
        '''
        CaseCommon.audio_analysis(cid, self.api.user_list, channels, samepleRate, registered_time,
                                  ProfileEnum.onRecordFrame)

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235933&view=table
    通话前或者通话中设置pub开关为false后主动离开，再次入会看是否有质量透明数据上报
    '''
    def test_audio_media_pub_leave_state(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        self.api.assert_error(self.api.user_list[0].LeaveChannel())
        time.sleep(2)
        self.api.SingleUserJoinChannle(self.task_cases_id, 0)

        self.api.EnableLocalAudio(True)
        self.api.SetRecordDeviceMute(False)

        '''设备0上报采集的音频信息'''
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        '''
        等待一段时间，透明数据2秒上报一次，多收集几组数据求平均来确保数据的准确性
        '''
        time.sleep(config.ReportTime)
        '''
        根据cname ,回调方法名， uid 查询到设备0本地音频上报的信息
        获取到json信息后，计算得到上报的码率，采样率的平均值
        '''
        bit_rate, sent_volume = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("发送码率: " + str(bit_rate))
        self.OutputUtils.print("发送音量: " + str(sent_volume))

        if bit_rate == 0 or sent_volume == 0:
            raise BaseException("通话前或者通话中设置pub开关为false后主动离开，再次入会看音频质量透明数据上报，码率应大于0")

        '''
        此时录制的音频有系统声音，是否有声音的断言判断还是有声音的
        '''
        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235933&view=table
    通话前或者通话中设置pub开关为false后主动离开，再次入会看是否有音量提示信息上报
    '''
    def test_audio_media_pub_leave_indication(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        '''
        此用例检测远端音量提示回调，因此需要对端用户也离会，清除掉Pub状态
        '''
        self.api.assert_error(self.api.user_list[0].LeaveChannel())
        self.api.assert_error(self.api.user_list[1].LeaveChannel())
        time.sleep(2)
        self.api.SingleUserJoinChannle(self.task_cases_id, 0)
        self.api.SingleUserJoinChannle(self.task_cases_id, 1)

        self.api.EnableLocalAudio(True)
        self.api.SetRecordDeviceMute(False)

        '''
        开启音量提示
        '''
        self.api.assert_error(self.api.user_list[0].EnableAudioVolumeIndication(True, 1000))
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id, ProfileEnum.onRemoteAudioVolumeIndication)
        local_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id, ProfileEnum.onLocalAudioVolumeIndication)

        self.OutputUtils.print("远端音量提示:" + str(remote_volume_indication))

        if len(remote_volume_indication) > 0:
            speaker_list = list(map(lambda x: int(json.loads(x["_source"]["data"])["uid"]), remote_volume_indication))
            total_volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["total_volume"]), remote_volume_indication))
            self.OutputUtils.print("远端说话者数量:" + str(speaker_list))
            self.OutputUtils.print("混音后的音量:" + str(total_volume_list))
            total_volume = mean(total_volume_list)

            if total_volume == 0:
                raise BaseException("通话前或者通话中设置pub开关为false后主动离开，再次入会期望有远端音量提示信息上报")
        else:
            raise BaseException("通话前或者通话中设置pub开关为false后主动离开，再次入会期望有远端音量提示信息上报")

        if len(local_volume_indication) > 0:
            volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["volume"]), remote_volume_indication))
            self.OutputUtils.print("本地提示的音量:" + str(volume_list))
            volume = mean(volume_list)

            if volume == 0:
                raise BaseException("通话前或者通话中设置pub开关为false后主动离开，再次入会期望有本地音量提示值大于0")
        else:
            raise BaseException("通话前或者通话中设置pub开关为false后主动离开，再次入会期望有本地音量提示信息上报")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235933&view=table
    通话前或者通话中设置pub开关为false后主动离开，再次入会看是否有音频回调文件生成
    '''
    def test_audio_media_pub_leave_callback(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(False)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(False)

        '''
        此用例检测远端音量提示回调，因此需要对端用户也离会，清除掉Pub状态
        '''
        self.api.assert_error(self.api.user_list[0].LeaveChannel())
        self.api.assert_error(self.api.user_list[1].LeaveChannel())
        time.sleep(2)
        '''
        生成pcm文件的时间戳，文件命名用到
        '''
        registered_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        开启音频回调，回调文件生成规则为回调类型+用户id+声道数+ 采样率+ 时间戳.pcm
        如 Mixed_12320_1_48000_20200814xxx.pcm
        '''
        self.api.user_list[0].SetAudioFrameObserver(uid=self.api.user_list[0].uid, curtime=registered_time)
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        self.api.SingleUserJoinChannle(self.task_cases_id, 0)
        self.api.SingleUserJoinChannle(self.task_cases_id, 1)

        self.api.EnableLocalAudio(True)
        self.api.SetRecordDeviceMute(False)

        time.sleep(8)
        '''
        获取pcm录制回调的采样率,声道数
        '''
        samepleRate, channels = CaseCommon.get_audio_callback_info(self.task_cases_id, self.api.user_list, ProfileEnum.onRecordFrame)
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))

        self.OutputUtils.print("RecordFrame sample rate, channels : " + str(samepleRate) + str("," + str(channels)))
        self.api.assert_error(self.api.user_list[0].EnableLocalAudio(False))
        '''
        关闭音频回调
        '''
        self.api.user_list[0].SetAudioFrameObserver(uid=self.api.user_list[0].uid, switch=False)
        time.sleep(5)
        '''
        record pcm playback pcm ,mixed pcm 文件压缩上传到服务端, 脚本可根据采样率，声道数，时间戳去服务端找到相应的文件
        服务端调用脚本分析生成的pcm 文件是否有声音
        '''
        CaseCommon.audio_analysis(cid, self.api.user_list, channels, samepleRate, registered_time,
                                  ProfileEnum.onRecordFrame)

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235469&view=table
    通话前设置pub开关为true，入会后查看音频透明质量数据是否正常 
    '''
    def test_audio_media_pub_on(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(True)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(True)

        self.api.EnableLocalAudio(True)
        '''设备0上报采集的音频信息'''
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        '''
        等待一段时间，透明数据2秒上报一次，多收集几组数据求平均来确保数据的准确性
        '''
        time.sleep(config.ReportTime)
        '''
        根据cname ,回调方法名， uid 查询到设备0本地音频上报的信息
        获取到json信息后，计算得到上报的码率，采样率的平均值
        '''
        bit_rate, sent_volume = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("发送码率: " + str(bit_rate))
        self.OutputUtils.print("发送音量: " + str(sent_volume))

        if bit_rate == 0 or sent_volume == 0:
            raise BaseException("Pub开关设置为False, 期望音量透明数据统计不回调，实际音量有值")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
   https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235469&view=table
   通话前/中设置pub开关为true，入会后查看音量提示回调等是否正常 
   '''
    def test_audio_media_pub_volume_indication_on(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        if args[2]:
            self.api.EnableMediaPub(True)
        cid = self.api.JoinChannle(self.task_cases_id)
        if not args[2]:
            self.api.EnableMediaPub(True)

        self.api.EnableLocalAudio(True)

        '''
        开启音量提示
        '''
        self.api.assert_error(self.api.user_list[0].EnableAudioVolumeIndication(True, 1000))
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                        ProfileEnum.onRemoteAudioVolumeIndication)
        local_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                       ProfileEnum.onLocalAudioVolumeIndication)

        self.OutputUtils.print("远端音量提示:" + str(remote_volume_indication))

        if len(remote_volume_indication) > 0:
            speaker_list = list(map(lambda x: int(json.loads(x["_source"]["data"])["uid"]), remote_volume_indication))
            total_volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["total_volume"]), remote_volume_indication))
            self.OutputUtils.print("远端说话者数量:" + str(speaker_list))
            self.OutputUtils.print("混音后的音量:" + str(total_volume_list))
            total_volume = mean(total_volume_list)

            if total_volume == 0:
                raise BaseException("通话前或者通话中设置pub开关为true会期望有远端音量提示信息上报")
        else:
            raise BaseException("通话前或者通话中设置pub开关为true期望有远端音量提示信息上报")

        if len(local_volume_indication) > 0:
            volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["volume"]), remote_volume_indication))
            self.OutputUtils.print("本地提示的音量:" + str(volume_list))
            volume = mean(volume_list)

            if volume == 0:
                raise BaseException("通话前或者通话中设置pub开关为true期望有本地音量提示值大于0")
        else:
            raise BaseException("通话前或者通话中设置pub开关为true期望有本地音量提示信息上报")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235905&view=table
    通话前enablelocalaudio为false，设置pub为false，建立通话 
    '''
    def test_audio_off_media_pub_off(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        self.api.EnableMediaPub(False)
        self.api.EnableLocalAudio(False)
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_audio_start = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                        ProfileEnum.onUserAudioStart)

        if len(remote_audio_start) > 0:
            raise BaseException("期望对端未收到本端onuseraudiostart信令")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if not is_slience:
            raise BaseException("期望没有声音, 实际有声音")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235960&view=table
    通话前enablelocalaudio为false，设置pub为false，建立通话后再把pub设置为true，最后把enablelocalaudio设置为true 
    '''
    def test_audio_off_media_pub_off_on(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        self.api.EnableMediaPub(False)
        self.api.EnableLocalAudio(False)
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))

        cid = self.api.JoinChannle(self.task_cases_id)

        self.api.EnableMediaPub(True)
        self.api.EnableLocalAudio(True)
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_audio_start = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                        ProfileEnum.onUserAudioStart)

        if len(remote_audio_start) == 0:
            raise BaseException("期望对端收到本端onuseraudiostart信令, 实际未收到")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9235960&view=table
    通话前先mute，打开静音回调音量，然后加入房间看mute状态 
    '''
    def test_audio_mute_volume_indication_on(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        self.api.MuteLocalAudioStream(True)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id, uid=self.api.user_list[1].info["userId"]))

        cid = self.api.JoinChannle(self.task_cases_id)

        '''
        开启音量提示
        '''
        self.api.assert_error(self.api.user_list[0].EnableAudioVolumeIndication(True, 1000))
        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id,
                                                                  uid=self.api.user_list[0].info["userId"]))
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        time.sleep(config.ReportTime)
        remote_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                        ProfileEnum.onRemoteAudioVolumeIndication, uid=self.api.user_list[1].info["userId"])
        local_volume_indication = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                       ProfileEnum.onLocalAudioVolumeIndication, uid=self.api.user_list[0].info["userId"])

        self.OutputUtils.print("远端音量提示:" + str(remote_volume_indication))

        if len(remote_volume_indication) > 0:
            raise BaseException("Mute后期望没有远端音量提示信息上报")

        if len(local_volume_indication) > 0:
            volume_list = list(
                map(lambda x: int(json.loads(x["_source"]["data"])["volume"]), local_volume_indication))
            self.OutputUtils.print("本地提示的音量:" + str(volume_list))
            volume = mean(volume_list)

            if volume > 0:
                raise BaseException("Mute时本地音量提示值期望是0")
        else:
            raise BaseException("期望有本地音量提示信息上报")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9244185&view=table
    通话前先mute，pub开关关闭，然后加入房间
    '''
    def test_audio_pub_off_mute(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        self.api.MuteLocalAudioStream(True)
        self.api.EnableMediaPub(False)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        self.api.MuteLocalAudioStream(False)

        time.sleep(config.ReportTime)
        remote_mute = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                                        ProfileEnum.onUserAudioMute)
        if len(remote_mute) > 0:
            raise BaseException("期望没有远端Mute信令")
        self.api.EnableMediaPub(False)
        time.sleep(3)
        remote_mute1 = self.api.user_list[0].GetProfileData(self.task_cases_id,
                                                           ProfileEnum.onUserAudioMute)

        if len(remote_mute1) > 0:
            raise BaseException("期望有远端Mute信令")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9245116&view=table
    伴音不走辅流，pub开关操作逻辑验证 
    '''
    def test_audio_pub_off_audio_mixing(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)
        self.api.StartAudioMixing()
        self.api.EnableMediaPub(False)
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())

        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("接收码率: " + str(bit_rate))
        self.OutputUtils.print("接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("伴音走主流+ pub 关闭，期望伴音不发送")

        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        打开MediaPub
        '''
        self.api.EnableMediaPub(True)
        time.sleep(5)
        bit_rate1, sent_volume1 = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("发送码率: " + str(bit_rate1))
        self.OutputUtils.print("发送音量: " + str(sent_volume1))

        if bit_rate1 == 0 or sent_volume1 == 0:
            raise BaseException("伴音走主流+ pub true，期望伴音发送")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9245116&view=table
    伴音不走辅流，pub开关操作逻辑验证 
    '''
    def test_audio_pub_off_audio_mixing(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)
        self.api.StartAudioMixing()
        self.api.EnableMediaPub(False)
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())

        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("接收码率: " + str(bit_rate))
        self.OutputUtils.print("接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("伴音走主流+ pub 关闭，期望伴音不发送")

        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        打开MediaPub
        '''
        self.api.EnableMediaPub(True)
        time.sleep(5)
        bit_rate1, sent_volume1 = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("发送码率: " + str(bit_rate1))
        self.OutputUtils.print("发送音量: " + str(sent_volume1))

        if bit_rate1 == 0 or sent_volume1 == 0:
            raise BaseException("伴音走主流+ pub true，期望伴音发送")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9246188&view=table
    伴音走辅流，pub开关操作逻辑验证
    '''
    def test_audio_pub_off_audio_mixing_sub(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)
        self.api.StartAudioMixing(audioType=1)
        self.api.EnableMediaPub(False)
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())

        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("接收码率: " + str(bit_rate))
        self.OutputUtils.print("接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("伴音走辅流+ pub 关闭，期望伴音不发送")

        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        打开MediaPub
        '''
        self.api.EnableMediaPub(True)
        time.sleep(5)
        bit_rate1, sent_volume1 = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("发送码率: " + str(bit_rate1))
        self.OutputUtils.print("发送音量: " + str(sent_volume1))

        if bit_rate1 == 0 or sent_volume1 == 0:
            raise BaseException("伴音走主流+ pub true，期望伴音发送")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    https://tc.hz.netease.com/#/project/885/case?path=/0/6848037/7241707/9234686&caseId=9245116&view=table
    伴音不走辅流，pub开关操作逻辑验证 
    '''
    def test_audio_pub_off_audio_effect(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        '''
        清空上报数据
        '''
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        设置设备0的上报地址，使用cname进行数据隔离
        '''
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id))

        cid = self.api.JoinChannle(self.task_cases_id)

        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)
        self.api.PlayEffect(effect_id=1)
        self.api.EnableMediaPub(False)
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())

        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("接收码率: " + str(bit_rate))
        self.OutputUtils.print("接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("音效走主流+ pub 关闭，期望音效不发送")

        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''
        打开MediaPub
        '''
        self.api.EnableMediaPub(True)
        time.sleep(5)
        bit_rate1, sent_volume1 = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("发送码率: " + str(bit_rate1))
        self.OutputUtils.print("发送音量: " + str(sent_volume1))

        if bit_rate1 == 0 or sent_volume1 == 0:
            raise BaseException("音效走主流+ pub true，期望音效发送")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")

    '''
    通话过程中切换pub开关状态后切换房间
    '''
    def test_audio_pub_off_switch(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''设备1加入房间1, 发布音视频流，建立音视频房间'''
        cid = self.api.SingleUserJoinChannle(self.task_cases_id, 1)

        ApiCommon.assert_error(self.api.user_list[1].EnableLocalAudio(True))
        ApiCommon.assert_error(self.api.user_list[1].EnableLocalVideo(True))

        '''设备0加入房间0'''
        '''直播模式观众切房间'''
        self.api.assert_error(self.api.user_list[0].SetChannelProfile(1))
        self.api.assert_error(self.api.user_list[0].SetClientRole(1))
        self.api.SingleUserJoinChannle(self.task_cases_id + 100, 0)
        self.api.EnableMediaPub(False)

        '''设备0切换到房间1'''
        self.api.assert_error(self.api.user_list[0].SwitchChannel(self.task_cases_id))
        time.sleep(3)
        self.api.assert_error(self.api.user_list[0].SetClientRole(0))
        ApiCommon.assert_error(self.api.user_list[0].SetProfile())
        ApiCommon.assert_error(self.api.user_list[0].SetReportUrl(task_cases_id=self.task_cases_id))
        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("发送码率: " + str(bit_rate))
        self.OutputUtils.print("发送音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("Pub开关设置为False, 期望音量透明数据统计不回调，实际音量有值")

        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)
        self.api.EnableMediaPub(True)
        time.sleep(config.ReportTime)
        bit_rate1, sent_volume1 = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)
        self.OutputUtils.print("Pub True后发送码率: " + str(bit_rate1))
        self.OutputUtils.print("Pub True后发送音量: " + str(sent_volume1))

        if bit_rate1 == 0 or sent_volume1 == 0:
            raise BaseException("Pub开关设置True, 期望声音有值")

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    def test_audio_pub_off_media_relay(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''加入房间'''
        cid = self.api.SingleUserJoinChannle(self.task_cases_id, 1)

        ApiCommon.assert_error(self.api.user_list[1].EnableLocalAudio(True))
        ApiCommon.assert_error(self.api.user_list[1].EnableLocalVideo(True))

        self.api.SingleUserJoinChannle(self.task_cases_id + 200, 0)
        self.api.assert_error(self.api.user_list[0].EnableMediaPub(False))
        self.api.assert_error(self.api.user_list[0].EnableLocalAudio(True))
        self.api.assert_error(self.api.user_list[0].StartChannelMediaRelay(src_channel_name=self.task_cases_id + 200, src_uid=self.api.user_list[0].info["userId"],
                                                     dst_channel_names=self.task_cases_id, dst_uids=self.api.user_list[0].info["userId"]))
        time.sleep(2)
        self.api.user_list[1].SubscribeRemoteAudioStream(self.api.user_list[0].info["userId"], True)
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        ApiCommon.assert_error(self.api.user_list[1].SetProfile())
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id))
        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("Pub False Media Relay后接收码率: " + str(bit_rate))
        self.OutputUtils.print("Pub False Media Relay后接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("Pub开关设置为False, 期望Media Relay后 接收端没有音频信息")
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        self.api.EnableMediaPub(True)
        time.sleep(config.ReportTime)
        bit_rate1, sent_volume1 = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("Pub True Media Relay后接收码率: " + str(bit_rate1))
        self.OutputUtils.print("Pub True Media Relay后接收音量: " + str(sent_volume1))

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")


    def test_audio_media_relay_pub_off(self, args):
        self.api.initialize(channel_name=self.task_cases_id)
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        '''加入房间'''
        cid = self.api.SingleUserJoinChannle(self.task_cases_id, 1)

        ApiCommon.assert_error(self.api.user_list[1].EnableLocalAudio(True))
        ApiCommon.assert_error(self.api.user_list[1].EnableLocalVideo(True))

        self.api.SingleUserJoinChannle(self.task_cases_id + 200, 0)
        self.api.assert_error(self.api.user_list[0].EnableLocalAudio(True))
        self.api.assert_error(self.api.user_list[0].StartChannelMediaRelay(src_channel_name=self.task_cases_id + 200,
                                                                           src_uid=self.api.user_list[0].info["userId"],
                                                                           dst_channel_names=self.task_cases_id,
                                                                           dst_uids=self.api.user_list[0].info[
                                                                               "userId"]))
        time.sleep(2)
        self.api.assert_error(self.api.user_list[0].EnableMediaPub(False))
        self.api.user_list[1].SubscribeRemoteAudioStream(self.api.user_list[0].info["userId"], True)
        CaseCommon.audio_record_start(self.api.user_list, self.task_cases_id)

        ApiCommon.assert_error(self.api.user_list[1].SetProfile())
        ApiCommon.assert_error(self.api.user_list[1].SetReportUrl(task_cases_id=self.task_cases_id))
        time.sleep(config.ReportTime)
        bit_rate, sent_volume = self.api.get_remote_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("Pub False Media Relay后接收码率: " + str(bit_rate))
        self.OutputUtils.print("Pub False Media Relay后接收音量: " + str(sent_volume))

        if bit_rate > 0 or sent_volume > 0:
            raise BaseException("Pub开关设置为False, 期望Media Relay后 接收端没有音频信息")
        self.api.user_list[0].ClearProfileData(task_cases_id=self.task_cases_id)

        self.api.EnableMediaPub(True)
        time.sleep(config.ReportTime)
        bit_rate1, sent_volume1 = self.api.get_local_audio_info(self.api.user_list[0], self.task_cases_id)

        self.OutputUtils.print("Pub True Media Relay后接收码率: " + str(bit_rate1))
        self.OutputUtils.print("Pub True Media Relay后接收音量: " + str(sent_volume1))

        is_slience = CaseCommon.audio_record_analysis(cid, self.api.user_list, self.task_cases_id)
        if is_slience:
            raise BaseException("期望有声音，实际无声")



    def tearDown(self):
        self.OutputUtils.print("teardown")
        self.api.LeaveChannel()


if __name__ == "__main__":
    data = {
        "user_list": [],
        "channel_name": "1123116",
        "check_user_len": 4,
        "data": [],
        "task_cases_id": 1000385,
        "parameter": []
    }
    data["user_list"].append(config.IP9)
    data["user_list"].append(config.IP8)

    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub", True, "通话前设置pub开关为false"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_volume_indication", True, "通话前设置pub开关为false"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_audio_callback", True, "通话前设置pub开关为false"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub", False, "通话中设置pub开关为false"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_volume_indication", False, "通话中设置pub开关为false"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_audio_callback", False, "通话中设置pub开关为false"]


    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_indication", True,
                         "通话前设置pub开关为false后主动离开，再次入会看是否有音量提示信息上报 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_indication", False,
                         "通话中设置pub开关为false后主动离开，再次入会看是否有音量提示信息上报 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_callback", False,
                         "通话中设置pub开关为false后主动离开，再次入会看是否有音频回调信息 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_callback", True,
                         "通话前设置pub开关为false后主动离开，再次入会看是否有音频回调信息 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_on", True,
                         "通话前设置pub开关为true，入会后查看音量质量透明数据"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_on", False,
                         "通话中设置pub开关为true，入会后查看音量质量透明数据"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_volume_indication_on", False,
                         "通话中设置pub开关为true，入会后查看音量提示信息"]

    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_state", True, "通话前设置pub开关为false后主动离开，再次入会看默认状态是否恢复为true "]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_pub_leave_state", False, "通话中设置pub开关为false后主动离开，再次入会看默认状态是否恢复为true "]
    data["parameter"] = ['Pub和采集分离', "test_audio_off_media_pub_off", "通话前enablelocalaudio为false，设置pub为false，建立通话 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_off_media_pub_off_on", "通话前enablelocalaudio为false，设置pub为false，建立通话后再把pub设置为true，最后把enablelocalaudio设置为true "]


    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_mixing", "伴音不走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_mixing_sub", "伴音走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_effect", "音效走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_switch", "音效走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_media_relay", "通话过程中切换pub开关状态后跨房间推流"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_relay_pub_off", "通话过程中切换pub开关状态后跨房间推流"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_mute", "通话前先mute，pub开关关闭，然后加入房间"]
    data["parameter"] = ['Pub和采集分离', "test_audio_mute_volume_indication_on", "通话前enablelocalaudio为false，设置pub为false，建立通话后再把pub设置为true，最后把enablelocalaudio设置为true "]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_mute", "通话前先mute，pub开关关闭，然后加入房间 "]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_mixing", "伴音不走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_mixing_sub", "伴音走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_audio_effect", "音效走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_switch", "音效走辅流，pub开关操作逻辑验证"]
    data["parameter"] = ['Pub和采集分离', "test_audio_pub_off_media_relay", "通话过程中切换pub开关状态后跨房间推流"]
    data["parameter"] = ['Pub和采集分离', "test_audio_media_relay_pub_off", "通话过程中切换pub开关状态后跨房间推流"]









    AudioMediaPubSetting().run(**data)
