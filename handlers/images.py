#! /usr/bin/env python
# coding: utf-8
# author:zhihua

import traceback, os, json, os, uuid
from conf import config
from base import BaseHandler


class UploadImagesHandler(BaseHandler):
    def get(self):
        try:
            self.write(config.UPLOADPAGE)
        except Exception as e:
            self.send_status_message(-3, traceback.format_exc())
            self.log.error(traceback.format_exc())

    def post(self):
        try:
            upload_path = "/opt/ABBYY/FREngine11/Samples/SampleImages"
            file_metas = self.request.files.get('file', None)
            if not file_metas:
                return self.send_status_message(-2, 'invalid file content or file name.')
            meta = file_metas[0]
            uname_pfix = str(uuid.uuid1())
            sfile = uname_pfix + os.path.splitext(meta['filename'])[1]  # 源文件
            tfile = 'c_' + uname_pfix + '.pdf'  # 目标文件
            with open(os.path.join(upload_path, sfile), 'wb') as f:
                f.write(meta['body'])
                f.flush()
            # 转化
            self.log.info('start to convert to pdf %s %s ' % (sfile, tfile))
            os.system("cd /opt/ABBYY/FREngine11/Samples/Java/Hello && sh run.sh %s %s" % (sfile, tfile))
            if not os.path.isfile(os.path.join(upload_path, tfile)):
                self.log.warning('convert to pdf failed..')
                return self.send_status_message(-3, 'convert to pdf failed!')
            self.log.info('end to convert pdf start to download !')
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + tfile)
            with open(os.path.join(upload_path, tfile), 'rb') as f:
                while True:
                    data = f.read(2048)
                    if not data:
                        break
                    self.write(data)
            self.finish()
        except Exception as e:
            self.log.error(traceback.format_exc())
            self.send_status_message(-2, traceback.format_exc())
            print traceback.format_exc()

