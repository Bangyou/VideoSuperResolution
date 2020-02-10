# ##############################################################################
#  Copyright (c) 2020. LoSealL All Rights Reserved.
#  Author: Wenyi Tang
#  Email: wenyitang@outlook.com
#  Date: 2020 - 2 - 5
# ##############################################################################
import os

if not os.getcwd().endswith('UTest'):
  os.chdir('UTest')
from VSR.DataLoader import Dataset, Loader
from VSR.Model import get_model
from VSR.Backend import DATA_FORMAT

def test_train_srcnn():
  data = Dataset('data')
  data.include_reg('set5')
  ld = Loader(data, scale=2)
  ld.set_color_space('lr', 'L')
  ld.set_color_space('hr', 'L')
  m = get_model('srcnn')(scale=2, channel=1)
  with m.executor as t:
    config = t.query_config({})
    config.epochs = 5
    config.steps = 10
    if DATA_FORMAT == 'channels_first':
      config.batch_shape = [16, 1, 16, 16]
    else:
      config.batch_shape = [16, 16, 16, 1]
    t.fit([ld, None], config)


def test_infer_srcnn():
  m = get_model('srcnn')(scale=2, channel=3)
  data = Dataset('data')
  data.include_reg('set5')
  ld = Loader(data, scale=2)
  with m.executor as t:
    config = t.query_config({})
    t.infer(ld, config)


if __name__ == '__main__':
  test_infer_srcnn()
  test_train_srcnn()
