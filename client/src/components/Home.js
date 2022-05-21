import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { HOST } from '../common';
import AddChannel from './AddChannel';
import DeleteButton from './DeleteButton';
import DownloadControls, {
  DOWNLOADING,
  NOT_DOWNLOADING,
  DOWNLOADED,
} from './DownloadControls';

const Home = () => {
  let [channels, setChannels] = useState([]);
  const [isSubscribed, setIsSubscribed] = useState();

  useEffect(() => {
    (async () => {
      let receivedChannels = await fetch(`${HOST}/videos`).then((res) =>
        res.json()
      );

      // in-progress video downloads should reset on page refreshes
      receivedChannels.forEach((channel) => {
        channel.videos.forEach((videoDatum) => {
          videoDatum.download_status =
            videoDatum.download_status === DOWNLOADING
              ? NOT_DOWNLOADING
              : videoDatum.download_status;
        });
      });
      setChannels(receivedChannels);
    })();
  }, [isSubscribed]);

  const onChannelAdded = (channelData) => {
    // avoid adding undefined values and duplicates
    if (
      channelData &&
      !channels.some(({ channel: { id } }) => id === channelData.channel.id)
    ) {
      setChannels([...channels, channelData]);
    }
  };
 const handleDeleteRequest = async (id) => {
    try {
      const resp = await fetch(`${HOST}/watchlist`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id }),
      });
      if (resp.ok) {
        removeChannel(id);
        setIsSubscribed(!isSubscribed);
      }
    } catch (e) {
      console.log(e, 'Failed to delete channel');
    }
  };

  const removeChannel = (channelId) => {
    channels = channels.filter((element) => {
      return element.id !== channelId;
    });
  };

  const onVideoDownload = (video) => {
    const newChannels = updateVideoObj(channels, video.id, {
      ...video,
      download_status: DOWNLOADING,
    });
    setChannels(newChannels);

    fetch(`${HOST}/download-video?videoid=${video.id}`).then((resp) => {
      const newChannels = updateVideoObj(channels, video.id, {
        ...video,
        download_status: resp.ok ? DOWNLOADED : NOT_DOWNLOADING,
      });
      setChannels(newChannels);
    });
  };

    });
  };

  return (
    <>
      <AddChannel onChannelAdded={onChannelAdded} />

      {channels.map(({ channel: { name, id }, videos }) => (
        <ChannelContainer key={id}>
          <Channel>
            <h3>{name}</h3>
            <DeleteButton
              handleDeleteRequest={() => {
                handleDeleteRequest(id);
              }}
            />
          </Channel>
          <VideosContainer>
            {videos.map((video) => (
              <VideoItem key={video.id}>
                <LinkWrapper
                  href={'https://www.youtube.com/watch?v=' + video.id}
                  target="_blank"
                >
                  <Thumbnail src={video.thumbnail} />
                  <VideoTitle>{video.title}</VideoTitle>
                </LinkWrapper>
                <DownloadControls
                  video={video}
                  onDownload={() => onVideoDownload(video)}
                ></DownloadControls>
              </VideoItem>
            ))}
          </VideosContainer>
        </ChannelContainer>
      ))}
    </>
  );
};

export default Home;

const ChannelContainer = styled.div`
  // padding-top: 30px;
  padding: 10px;
`;

const VideosContainer = styled.div`
  width: 100%;
  overflow-x: auto;
  white-space: nowrap;
  overflow-y: hidden;
`;

const VideoItem = styled.div`
  display: inline-block;
  vertical-align: top;
  white-space: break-spaces;
  margin: 0 10px 10px 0;
  width: 220px;
`;

const Thumbnail = styled.img`
  width: 100%;
  display: block;
`;

const LinkWrapper = styled.a`
  &:any-link {
    color: black;
    text-decoration: none;
  }
`;

const Channel = styled.div`
  display: flex;
  align-content: center;
  justify-content: flex-start;
  align-items: center;
`;
const VideoTitle = styled.span`
  display: inline-block;
  height: 45px;
  overflow: hidden;
`;

/* Accepts a channels array and returns a copy of it with given video object updated */
const updateVideoObj = (channels, videoId, newValue) => {
  return channels.map((channel) => {
    return {
      ...channel,
      videos: channel.videos.map((video) => {
        if (video.id === videoId) {
          return { ...newValue };
        }
        return video;
      }),
    };
  });
};


