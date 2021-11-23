from typing import Union
import airquality.api.model.purpleair as p
import airquality.api.model.atmotube as a
import airquality.api.model.thingspeak as t

# DEFINE A UNION TYPE FOR THE RESPONSE MODEL BUILDER
RESP_MODEL_BUILDER_TYPE = Union[
    p.PurpleairAPIResponseModelBuilder,
    a.AtmotubeAPIResponseModelBuilder,
    t.ThingspeakAPIResponseModelBuilder
]

# DEFINE A UNION TYPE FOR THE RESPONSE MODEL
RESP_MODEL_TYPE = Union[
    p.PurpleairAPIResponseModel,
    a.AtmotubeResponseModel,
    t.ThingspeakChannel1AResponseModel,
    t.ThingspeakChannel1BResponseModel,
    t.ThingspeakChannel2AResponseModel,
    t.ThingspeakChannel2BResponseModel
]
