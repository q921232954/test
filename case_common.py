import requests
import json
from utils.output_utils import OutputUtils
from utils.http_utils import HttpUtils
from utils.time_utils import TimeUtils
import config
import time
from api_common.api_common import ApiCommon
from profile1.ProfileEnum import ProfileEnum
from numpy import mean
'''
Case相关操作
'''


class CaseCommon:
    '''
    判断图片是否纯黑色
    '''
    @staticmethod
    def is_black(cid, c_path):
        url = config.ASSERT_NODE + "is_black?cid=" + str(cid) + "&file=" + c_path
        data = HttpUtils.get(url)
        OutputUtils.print(url)
        OutputUtils.print(data)

        color_black = data["is_black"]
        return color_black

    '''
    判断图片是否纯白色
    '''
    @staticmethod
    def is_white(cid, c_path):
        url = config.ASSERT_NODE + "is_white?cid=" + str(cid) + "&file=" + c_path
        data = HttpUtils.get(url)

        OutputUtils.print(url)
        OutputUtils.print(data)

        color_white = data["is_white"]
        return color_white

    '''
    判断音频文件是否有声音
    '''
    @staticmethod
    def is_slience(cid, c_path):
        url = config.ASSERT_NODE + "slience?cid=" + str(cid) + "&file=" + c_path
        OutputUtils.print(url)
        time.sleep(2)
        data = HttpUtils.get(url)


        OutputUtils.print(data)

        audio_slience = data["slience"]
        return audio_slience

    '''
    获取图片长宽
    '''
    @staticmethod
    def get_image_size(cid, c_path):
        sizeUrl = config.ASSERT_NODE + "get_image_size?cid=" + str(cid) + "&file=" + c_path
        OutputUtils.print("获取图片尺寸" + sizeUrl)
        dataSize = HttpUtils.get(sizeUrl)
        OutputUtils.print(dataSize)
        snapshot_width = dataSize["width"]
        snapshot_height = dataSize["height"]

        return snapshot_width, snapshot_height

    '''
    获取图片相似度
    SSIM（structural similarity）结构相似性，也是一种全参考的图像质量评价指标，它分别从亮度、对比度、结构三方面度量两幅图像相似性，其值越大越好，最大为1
    '''
    @staticmethod
    def get_image_ssim(cid, path1, path2):
        diffUrl = config.ASSERT_NODE + "ssim?cid=" + str(cid) + "&file=" + path1 + "&file_diff=" + path2
        dataDiff = HttpUtils.get(diffUrl)
        OutputUtils.print(diffUrl)
        OutputUtils.print(dataDiff)

        snapshot_score = dataDiff["score"]

        return snapshot_score

    '''
    根据图片生成规程来获取文件名
    Windows端是sdk自动生成的文件名，只能根据回调方法获取文件名
    其它3端是在回调方法中实现了截图，按照local/remote + main/sub +channel + userid等规则来实现截图并生成文件名
    '''
    @staticmethod
    def get_file_name(task_cases_id, user,  streamType: int=0, videoType: int=0, channel: str="", curtime: str="", userId: str="", index=0):
        if user.platform == config.WINDOWS:
            snapshot_result = CaseCommon.GetCallbackData(task_cases_id=task_cases_id, call_back_method=ProfileEnum.onTakeSnapshotResult)
            OutputUtils.print("截图回调地址:" + str(snapshot_result))
            if snapshot_result:
                path = json.loads(snapshot_result[index]["_source"]["data"])["image"]
                p = CaseCommon.path_replace(path)
                filename = p.split("/")[-1]
            else:
                filename = ''
        else:
            filename = ""
            if user.platform == config.ANDROID or user.platform == config.IOS or user.platform == config.MAC:
                if videoType == 0:
                    if channel == "":
                        prefix = "local_" + str(userId)
                    else:
                        prefix = "local_" + channel + "_" + str(userId)

                else:
                    if channel == "":
                        prefix = "remote_" + str(userId)
                    else:
                        prefix = "remote_" + channel + "_" + str(userId)

                if streamType == 0:
                    if user.platform == config.ANDROID or user.platform == config.MAC:
                        filename = prefix + "_" + "main_" + curtime + ".jpg"
                        OutputUtils.print(filename)
                    else:
                        filename = prefix + "_" + "main_" + curtime + ".png"
                else:
                    if user.platform == config.ANDROID or user.platform == config.MAC:
                        filename = prefix + "_" + "sub_" + curtime + ".jpg"
                    else:
                        filename = prefix + "_" + "sub_" + curtime + ".png"
        return filename

    @staticmethod
    def get_canvas_file_name(task_cases_id, user, streamType: int = 0, videoType: int = 0, channel: str = "",
                             curtime: str = "", userId: str = "", index=0):
        filename = ""
        if videoType == 0:
            if channel == "":
                prefix = "local_" + str(userId)
            else:
                prefix = "local_" + channel + "_" + str(userId)
        else:
            if channel == "":
                prefix = "remote_" + str(userId)
            else:
                prefix = "remote_" + channel + "_" + str(userId)

        if streamType == 0:
            if user.platform == config.ANDROID :
                filename = prefix + "_" + "main_" + curtime + ".jpg"
                OutputUtils.print(filename)
            elif user.platform == config.IOS:
                filename = prefix + "_" + "main_" + curtime + ".png"
                OutputUtils.print(filename)
            else:
                filename = prefix + "_" + "main_" + curtime + ".bmp"
        else:
            if user.platform == config.ANDROID:
                filename = prefix + "_" + "sub_" + curtime + ".jpg"
            elif user.platform == config.IOS:
                filename = prefix + "_" + "sub_" + curtime + ".png"
            else:
                filename = prefix + "_" + "sub_" + curtime + ".bmp"
        return filename

    @staticmethod
    def path_replace(path: str):
        if '\\' in path:
            p = path.replace("\\", "/")
            return CaseCommon.path_replace(p)
        elif "//" in path:
            p = path.replace("//", "/")
            return CaseCommon.path_replace(p)
        else:
            return path

    '''
    获取各端本地截图路径
    '''
    @staticmethod
    def get_file_path(task_cases_id, user):
        if user.platform == config.WINDOWS:
            snapshot_result = CaseCommon.GetCallbackData(task_cases_id=task_cases_id,
                                                         call_back_method=ProfileEnum.onTakeSnapshotResult)
            if not snapshot_result:
                raise BaseException("文件路径为空")
            path = json.loads(snapshot_result[0]["_source"]["data"])["image"]
            p = CaseCommon.path_replace(path)
            filePath = p.split("/")[:-1]
            result = ""
            for i in filePath:
                result = result + i + "/"
            OutputUtils.print("转化后路径" + result)
            return result
        elif user.platform == config.ANDROID:
            path = "/sdcard/snapshot/"
            return path
        elif user.platform == config.MAC:
            path = ""
            return path
        elif user.platform == config.IOS:
            return "images"

    '''
    连续截2张图
    步骤1： 安卓,ios 设置画布
    步骤2： 截第一张图 TakeLocalSnapshot/TakeRemoteSnapshot
    步骤3： 根据截图文件命名规则，找到各端的截图并生成压缩文件并上传测试服务 ZipAssets && UploadAssets
    步骤4： 调用服务判断截图是否白屏 is_white
    步骤5： 调用服务判断截图是否黑屏 is_black
    步骤6： 截第二张图 TakeLocalSnapshot/TakeRemoteSnapshot 生成压缩文件并上传测试服务 ZipAssets && UploadAssets
    步骤7： 调用服务判断 第二张图 是否白屏 is_white 是否黑屏 is_black
    步骤8： 调用服务判断 第二张图 与第一张图 的相似度
    streamType 是指主辅流，videotype是指截本地还是远端，0是本地，1是远端
    remote_uid 是指远端截图的用户索引。
    '''
    @staticmethod
    def snapshot_analysis(task_cases_id, cid, user_list, streamType, videoType, channel, remote_uid):
        '''
        第一次截图
        '''
        snapshot_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)

        '''
        本地用户
        '''
        user = user_list[0]
        '''
        如果有远端用户, uid不为0
        '''
        if videoType != 0:
            remote_user = user_list[int(remote_uid)]
        user.SetReportUrl(task_cases_id=task_cases_id)

        if user.platform == config.ANDROID or user.platform == config.IOS:
            if videoType == 0:
                '''
                安卓, ios生成截图前需设置画布，否则无法生成截图
                '''
                # user.SetupLocalVideoCanvas(0)
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path1 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time, user.uid)
            else:
                #user.SetupRemoteVideoCanvas(remote_user.info["userId"], 0)
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path1 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time, remote_user.uid)
        else:
            if videoType == 0:
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path1 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time, user.uid)
            else:
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path1 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel,
                                                   snapshot_time, remote_user.uid)

        '''
        上传到服务端
        '''
        snapshot_path = CaseCommon.get_file_path(task_cases_id, user)
        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path1
        # else:
        zip_path = c_path1
        ApiCommon.assert_error(user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip"))
        time.sleep(2)
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                                          cid=str(cid),
                                          uid=user.uid,
                                          zip_name=str(cid) + ".zip")

        '''
        等待一段时间，防止服务端文件上传解压没完成
        '''
        time.sleep(6)
        snapshot_width, snapshot_height = CaseCommon.get_image_size(cid, c_path1)
        color_black = CaseCommon.is_black(cid, c_path1)
        if color_black:
            raise BaseException("截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path1)
        if color_white:
            raise BaseException("截图白屏")


        #c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time)

        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path1
        OutputUtils.print("第一次截图上传后的图片地址：" + access_url)

        '''
        第二次截图
        '''

        snapshot_time2 = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)

        '''
        第二次截图移动端不需要设置画布
        '''
        if videoType == 0:
            ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time2))
            time.sleep(2)
            c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2, user.uid)
        else:
            ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time2))
            time.sleep(2)
            c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel,
                                               snapshot_time2, remote_user.uid)


        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path2
        # else:
        zip_path = c_path2

        '''
        判断黑白屏
        上传
        '''
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                                          cid=str(cid),
                                          uid=user.uid,
                                          zip_name=str(cid) + ".zip")
        if videoType != 0:
            user = remote_user
        time.sleep(6)
        color_black = CaseCommon.is_black(cid, c_path2)
        if color_black:
            raise BaseException("第二次截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path2)
        if color_white:
            raise BaseException("第二次截图白屏")
        image_ssim_score = CaseCommon.get_image_ssim(cid, c_path1, c_path2)

        OutputUtils.print("当前截图类型 " + str(streamType) + "_" + str(videoType))
        if streamType != 1:
            if image_ssim_score > 0.999:
                raise ("两次截图画面相似度值接近1，画面内容相同")

        OutputUtils.print("图片相似度" + str(image_ssim_score))
        access_url2 = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path2
        OutputUtils.print("第二次截图上传后的图片地址：" + access_url2)
        if snapshot_width == 0 or snapshot_height == 0:
            raise BaseException("截图异常")

        return snapshot_width, snapshot_height

    '''
    截第一张图
    步骤1： 安卓,ios 设置画布
    步骤2： 截第一张图 TakeLocalSnapshot/TakeRemoteSnapshot
    步骤3： 根据截图文件命名规则，找到各端的截图并生成压缩文件并上传测试服务 ZipAssets && UploadAssets
    步骤4： 调用服务判断截图是否白屏 is_white
    步骤5： 调用服务判断截图是否黑屏 is_black
    user_index 代表要截图的设备，默认都截第一个设备的
    streamtype:0 是主流， 1 是辅流
    videotype是指截本地还是远端，0是本地，1是远端
    '''
    @staticmethod
    def snapshot_first_time(task_cases_id, cid, user_list, streamType, videoType, channel, remote_uid, user_index=0):
        '''
        第一次截图
        '''
        snapshot_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        安卓, ios生成截图前需设置画布，否则无法生成截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        else:
            user.SetReportUrl(task_cases_id=task_cases_id)
        if user.platform == config.ANDROID or user.platform == config.IOS:
            if videoType == 0:
                #user.SetupLocalVideoCanvas(0)
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time, user.uid)
            else:
                #user.SetupRemoteVideoCanvas(remote_user.info["userId"], 0)
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  remote_user.uid)
        else:
            if videoType == 0:
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time, user.uid)
            else:
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  remote_user.uid)

        snapshot_path = CaseCommon.get_file_path(task_cases_id, user)

        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path
        # else:
        zip_path = c_path
        '''
        截图打包成zip文件
        '''
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        '''
        zip文件上传测试服务
        '''
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                                          cid=str(cid),
                                          uid=user.uid,
                                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        snapshot_width, snapshot_height = CaseCommon.get_image_size(cid, c_path)

        color_black = CaseCommon.is_black(cid, c_path)
        if color_black:
            raise BaseException("截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path)
        if color_white:
            raise BaseException("截图白屏")

        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path
        OutputUtils.print("第一次截图上传后的图片地址：" + access_url)

        time.sleep(2)

        return snapshot_width, snapshot_height, c_path

    @staticmethod
    def snapshot_canvas_first_time(task_cases_id, cid, user_list, streamType, videoType, channel, remote_uid, user_index=0):
        '''
        第一次截图
        '''
        snapshot_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        安卓, ios生成截图前需设置画布，否则无法生成截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        else:
            user.SetReportUrl(task_cases_id=task_cases_id)
        if videoType == 0:
            ApiCommon.assert_error(user.TakeLocalCanvasSnapshot(streamType, user.uid, time=snapshot_time))
            time.sleep(2)
            c_path = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                              user.uid)
        else:
            ApiCommon.assert_error(user.TakeRemoteCanvasSnapshot(streamType, remote_user.uid, time=snapshot_time))
            time.sleep(2)
            c_path = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                              remote_user.uid)
        snapshot_path = ""
        if user.platform == config.ANDROID or user.platform == config.IOS:
            snapshot_path = CaseCommon.get_file_path(task_cases_id, user)

        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path
        # else:
        zip_path = c_path
        '''
        截图打包成zip文件
        '''
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        '''
        zip文件上传测试服务
        '''
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        snapshot_width, snapshot_height = CaseCommon.get_image_size(cid, c_path)

        color_black = CaseCommon.is_black(cid, c_path)
        if color_black:
            raise BaseException("截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path)
        if color_white:
            raise BaseException("截图白屏")

        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path
        OutputUtils.print("第一次截图上传后的图片地址：" + access_url)

        time.sleep(2)

        return snapshot_width, snapshot_height, c_path

    @staticmethod
    def snapshot_canvas_get_text(task_cases_id, cid, user_list, streamType, videoType, channel, remote_uid,
                                   user_index=0):
        '''
        第一次截图
        '''
        snapshot_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        安卓, ios生成截图前需设置画布，否则无法生成截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        else:
            user.SetReportUrl(task_cases_id=task_cases_id)
        if videoType == 0:
            ApiCommon.assert_error(user.TakeLocalCanvasSnapshot(streamType, user.uid, time=snapshot_time))
            time.sleep(2)
            c_path = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                     user.uid)
        else:
            ApiCommon.assert_error(user.TakeRemoteCanvasSnapshot(streamType, remote_user.uid, time=snapshot_time))
            time.sleep(2)
            c_path = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                     remote_user.uid)
        snapshot_path = ""
        if user.platform == config.ANDROID or user.platform == config.IOS:
            snapshot_path = CaseCommon.get_file_path(task_cases_id, user)

        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path
        # else:
        zip_path = c_path
        '''
        截图打包成zip文件
        '''
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        '''
        zip文件上传测试服务
        '''
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        snapshot_width, snapshot_height = CaseCommon.get_image_size(cid, c_path)

        color_black = CaseCommon.is_black(cid, c_path)
        if color_black:
            raise BaseException("截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path)
        if color_white:
            raise BaseException("截图白屏")

        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path
        OutputUtils.print("第一次截图上传后的图片地址：" + access_url)
        text = CaseCommon.get_snapshot_context(cid, c_path)

        time.sleep(2)

        return text

    '''
    截第二张图
    步骤2： 截第一张图 TakeLocalSnapshot/TakeRemoteSnapshot
    步骤3： 根据截图文件命名规则，找到各端的截图并生成压缩文件并上传测试服务 ZipAssets && UploadAssets
    步骤4： 调用服务判断截图是否白屏 is_white
    步骤5： 调用服务判断截图是否黑屏 is_black
    步骤6： 调用服务判断 第二张图 与第一张图 的相似度
    '''
    @staticmethod
    def snapshot_second_time(task_cases_id, cid, user_list, streamType, videoType, channel, c_path, remote_uid, user_index=0):

        '''
        第二次截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        snapshot_time2 = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)

        if user.platform == config.ANDROID or user.platform == config.IOS:
            if videoType == 0:
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time2))
                time.sleep(2)
                c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2,
                                                  user.uid, index=0)
            else:
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time2))
                time.sleep(2)
                c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2,
                                                   remote_user.uid, index=0)
        else:
            if videoType == 0:
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time2))
                time.sleep(2)
                c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2,
                                                  user.uid, index=0)
            else:
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time2))
                time.sleep(2)
                c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2,
                                                   remote_user.uid, index=0)

        #time.sleep(2)
        #c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2)
        snapshot_path = CaseCommon.get_file_path(task_cases_id, user)
        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path2
        # else:
        zip_path = c_path2
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        image_ssim_score = CaseCommon.get_image_ssim(cid, c_path, c_path2)
        access_url2 = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path2
        OutputUtils.print("第二次截图上传后的图片地址：" + access_url2)
        OutputUtils.print("图片相似度" + str(image_ssim_score))

        return image_ssim_score

    @staticmethod
    def snapshot_canvas_second_time(task_cases_id, cid, user_list, streamType, videoType, channel, c_path, remote_uid,
                             user_index=0):

        '''
        第二次截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        snapshot_time2 = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)

        if videoType == 0:
            ApiCommon.assert_error(user.TakeLocalCanvasSnapshot(streamType, user.uid, time=snapshot_time2))
            time.sleep(2)
            c_path2 = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel,
                                                      snapshot_time2,
                                                      user.uid, index=0)
        else:
            ApiCommon.assert_error(user.TakeRemoteCanvasSnapshot(streamType, remote_user.uid, time=snapshot_time2))
            time.sleep(2)
            c_path2 = CaseCommon.get_canvas_file_name(task_cases_id, user, streamType, videoType, channel,
                                                      snapshot_time2,
                                                      remote_user.uid, index=0)

        # time.sleep(2)
        # c_path2 = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time2)

        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path2
        # else:
        zip_path = c_path2
        snapshot_path = ""
        if user.platform == config.ANDROID or user.platform == config.IOS:
            snapshot_path = CaseCommon.get_file_path(task_cases_id, user)
            user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        else:
            user.ZipCanvasAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        image_ssim_score = CaseCommon.get_image_ssim(cid, c_path, c_path2)
        access_url2 = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path2
        OutputUtils.print("第二次截图上传后的图片地址：" + access_url2)
        OutputUtils.print("图片相似度" + str(image_ssim_score))

        return image_ssim_score

    '''
    获取图片文字信息
    '''
    @staticmethod
    def get_snapshot_context(cid, c_path):
        url = config.ASSERT_NODE + "get_text?cid=" + str(cid) + "&file=" + c_path
        OutputUtils.print(url)
        time.sleep(2)
        data = HttpUtils.get(url)
        OutputUtils.print(data)

        context = data["code"]
        return context

    '''
    获取截图内文字信息
    步骤1： 安卓,ios 设置画布
    步骤2： 截第一张图 TakeLocalSnapshot/TakeRemoteSnapshot
    步骤3： 根据截图文件命名规则，找到各端的截图并生成压缩文件并上传测试服务 ZipAssets && UploadAssets
    步骤4： 调用服务判断截图是否白屏 is_white
    步骤5： 调用服务判断截图是否黑屏 is_black
    步骤6： 调用服务获取截图文字信息 get_snapshot_context
    '''
    @staticmethod
    def snapshot_text_content(task_cases_id, cid, user_list, streamType, videoType, channel, remote_uid, user_index=0):
        '''
        第一次截图
        '''
        snapshot_time = TimeUtils.get_cur_time().strftime(TimeUtils.time_format2)
        '''
        安卓, ios生成截图前需设置画布，否则无法生成截图
        '''
        user = user_list[user_index]
        if remote_uid != 0 or user_index > 0:
            remote_user = user_list[int(remote_uid)]
            user.SetReportUrl(task_cases_id=task_cases_id)
        if user.platform == config.ANDROID or user.platform == config.IOS:
            if videoType == 0:
                #user.SetupLocalVideoCanvas(0)
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  user.uid)
            else:
                #user.SetupRemoteVideoCanvas(remote_user.info["userId"], 0)
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  remote_user.uid)
        else:
            if videoType == 0:
                ApiCommon.assert_error(user.TakeLocalSnapshot(streamType, user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  user.uid)
            else:
                ApiCommon.assert_error(user.TakeRemoteSnapshot(streamType, remote_user.uid, time=snapshot_time))
                time.sleep(2)
                c_path = CaseCommon.get_file_name(task_cases_id, user, streamType, videoType, channel, snapshot_time,
                                                  remote_user.uid)

        snapshot_path = CaseCommon.get_file_path(task_cases_id, user)

        # if user.platform == config.MAC:
        #     zip_path = "snapshot/" + c_path
        # else:
        zip_path = c_path
        '''
        截图打包成zip文件
        '''
        user.ZipAssets(path=snapshot_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)
        '''
        zip文件上传测试服务
        '''
        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=snapshot_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        if remote_uid != 0:
            user = remote_user
        color_black = CaseCommon.is_black(cid, c_path)
        if color_black:
            raise BaseException("截图黑屏")
        color_white = CaseCommon.is_white(cid, c_path)
        if color_white:
            raise BaseException("截图白屏")
        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + c_path
        OutputUtils.print("第一次截图上传后的图片地址：" + access_url)

        text = CaseCommon.get_snapshot_context(cid, c_path)


        time.sleep(2)

        return text


    @staticmethod
    def get_audio_callback_path(user):
        if user.platform == config.WINDOWS:
            path = ""
            return path
        elif user.platform == config.ANDROID:
            path = "/sdcard/callbackdump/"
            return path
        elif user.platform == config.MAC:
            path = ""
            return path
        elif user.platform == config.IOS:
            return ""

    @staticmethod
    def get_audio_record_path(user):
        if user.platform == config.WINDOWS:
            path =""
            return path
        elif user.platform == config.ANDROID:
            path = "/sdcard/"
            return path
        elif user.platform == config.MAC:
            path = ""
            return path
        elif user.platform == config.IOS:
            return ""

    @staticmethod
    def get_audio_dump_path(user):
        if user.platform == config.WINDOWS:
            path = ""
            return path
        elif user.platform == config.ANDROID:
            path = "dump"
            return path
        elif user.platform == config.MAC:
            path = ""
            return path
        elif user.platform == config.IOS:
            return "audioDump"

    @staticmethod
    def get_audio_dump_file_name(user):
        if user.platform == config.WINDOWS:
            path ="netease_nrtc_audio.dmp"
            return path
        elif user.platform == config.ANDROID:
            path = "nertc_audio.dump"
            return path
        elif user.platform == config.MAC:
            path = "mac_"
            return path
        elif user.platform == config.IOS:
            return "iOSAudioDump"

    @staticmethod
    def get_audio_record_file_name(user, suffix):
        if user.platform == config.WINDOWS:
            path ="pc_" + suffix
            return path
        elif user.platform == config.ANDROID:
            path = "android_" + suffix
            return path
        elif user.platform == config.MAC:
            path = "mac_" + suffix
            return path
        elif user.platform == config.IOS:
            return "ios_" + suffix

    @staticmethod
    def get_audio_callback_file(uid, channel, sample, curtime, callback_type):
        if callback_type == "onAudioFrameDidRecord":
            return "Record_" + uid + "_" + channel + "_" + sample + "_" + curtime + ".pcm"
        elif callback_type == "onAudioFrameWillPlayback":
            return "PlayBack_" + uid + "_" + channel + "_" + sample + "_" + curtime + ".pcm"
        elif callback_type == "onPlaybackAudioFrameBeforeMixing":
            return "PlayBackBeforeMixing_" + uid + "_" + channel + "_" + sample + "_" + curtime + ".pcm"
        elif callback_type == "onMixedAudioFrame":
            return "Mixed_" + uid + "_" + channel + "_" + sample + "_" + curtime + ".pcm"

    @staticmethod
    def get_ios_audio_callback_file(uid, channel, sample, curtime, callback_type):
        if callback_type == "onAudioFrameDidRecord":
            return "Record_" + uid + "_" + sample + "_" + channel  + "_" + curtime + ".pcm"
        elif callback_type == "onAudioFrameWillPlayback":
            return "PlayBack_" + uid + "_" + sample + "_" + channel + "_" + curtime + ".pcm"
        elif callback_type == "onPlaybackAudioFrameBeforeMixing":
            return "PlayBackBeforeMixing_" + uid + "_" + sample + "_" + channel + "_" + curtime + ".pcm"
        elif callback_type == "onMixedAudioFrame":
            return "Mixed_" + uid + "_" + sample + "_" + channel  + "_" + curtime + ".pcm"

    @staticmethod
    def get_audio_callback_info(cid, user_list, call_function):
        user = user_list[0]
        call_back_data = user.GetProfileData(cid, call_function)
        if call_back_data:
            sample_rate_list = list(map(lambda x: int(json.loads(x["_source"]["data"])["sample_rate"]),
                                        call_back_data))
            channelList = list(map(lambda x: int(json.loads(x["_source"]["data"])["channels"]),
                                   call_back_data))
            samepleRate = int(mean(sample_rate_list))
            channels = int(mean(channelList))
            OutputUtils.print(call_function + " sample rate: " + str(samepleRate))
        else:
            samepleRate = 0
            channels = 0
            raise BaseException("Callback method " + str(call_function) + "not found")
        return samepleRate, channels

    '''
    获取pcm回调是否有声音
    步骤1 获取音频回调文件路径和文件名
    步骤2 压缩音频文件，上传到测试服务
    步骤3 调用服务，判断获取到的文件是否有声音
    '''
    @staticmethod
    def audio_analysis(cid, user_list, channel, sample, curtime, cb_function):
        user = user_list[0]
        audio_callback_path = CaseCommon.get_audio_callback_path(user)
        if user_list[0].platform == config.IOS:
            zip_path = CaseCommon.get_ios_audio_callback_file(str(user.uid), str(channel), str(sample), curtime,
                                                              cb_function)
            OutputUtils.print("pcm 文件名:" + zip_path)
        else:
            zip_path = CaseCommon.get_audio_callback_file(str(user.uid), str(channel), str(sample), curtime,
                                                          cb_function)
        user.ZipAssets(path=audio_callback_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)

        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=audio_callback_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(6)
        audio_slience = CaseCommon.is_slience(cid, zip_path)
        if audio_slience:
            return BaseException("音频文件没有声音")
        access_url2 = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + zip_path
        OutputUtils.print("回调生成文件:" + access_url2)

    @staticmethod
    def audio_record_start(user_list, task_cases_id):

        user = user_list[0]
        audioformat = ".wav"
        if user.platform == config.ANDROID:
            file_path = "/sdcard/" + "android_" + str(task_cases_id) + audioformat
        elif user.platform == config.WINDOWS:
            file_path = "pc_" + str(task_cases_id) + audioformat
        elif user.platform == config.MAC:
            file_path = "mac_" + str(task_cases_id) + audioformat
        else:
            file_path = "ios_" + str(task_cases_id) + audioformat
        user.StartAudioRecordingWitchConfig(file_path, 32000, 0, 0, 0)

    '''
    获取录制音频是否有声音
    步骤3 调用服务，判断获取到的文件是否有声音
    '''
    @staticmethod
    def audio_record_analysis(cid, user_list, task_cases_id):
        user = user_list[0]
        user.StopAudioRecording()
        time.sleep(2)
        audio_rec_path = CaseCommon.get_audio_record_path(user)
        zip_path = CaseCommon.get_audio_record_file_name(user, str(task_cases_id) + ".wav")
        user.ZipAssets(path=audio_rec_path, file_names=zip_path, zip_name=str(cid) + ".zip")
        time.sleep(2)

        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=audio_rec_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        time.sleep(8)
        audio_slience = CaseCommon.is_slience(cid, zip_path)
        if audio_slience:
            OutputUtils.print("音频文件没有声音")
        access_url2 = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + zip_path
        OutputUtils.print("音频录制文件:" + access_url2)
        return audio_slience

    @staticmethod
    def audio_dump_upload(cid, user):
        audio_dump_path = CaseCommon.get_audio_dump_path(user)
        zip_path = CaseCommon.get_audio_dump_file_name(user)
        user.ZipAssets(path=audio_dump_path, file_names=zip_path, zip_name=str(cid) + ".zip")

        time.sleep(2)

        user.UploadAssets(config.UPLOAD_NODE + "/static_resources/upload", path=audio_dump_path,
                          cid=str(cid),
                          uid=user.uid,
                          zip_name=str(cid) + ".zip")
        access_url = config.RESOURCE_NODE + str(cid) + "/" + str(cid) + "/" + zip_path

        OutputUtils.print("音频Dump文件地址:" + access_url)



    @staticmethod
    def get(url, data1=None):
        result = requests.get(url, data=data1).text
        return json.loads(result)

    @staticmethod
    def GetCallbackData(task_cases_id: int, call_back_method, channel: str = -1, uid: int = -1):
        if config.SubRoomVersion:
            url = config.MAIN_NODE + """/es/getReportData?jobTaskId=%s&userId=%s&method=%s&channel_name=%s""" % (task_cases_id,
                                                                                        uid, call_back_method, channel)
        else:
            url = config.MAIN_NODE + """/es/getReportData?jobTaskId=%s&userId=%s&method=%s""" % (task_cases_id, uid, call_back_method)

        data = HttpUtils.get(url)
        return data["data"]
    



if __name__ == '__main__':
    pass
