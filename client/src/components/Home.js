import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { HOST } from '../common';
import AddChannel from './AddChannel';
import DownloadControls from './DownloadControls';

export const DOWNLOADED = 'downloaded';
export const DOWNLOADING = 'downloading';
export const NOT_DOWNLOADING = 'not_found';

const Home = () => {
  const [channels, setChannels] = useState([]);

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
  }, []);

  const onChannelAdded = (channelData) => {
    // avoid adding undefined values and duplicates
    if (
      channelData &&
      !channels.some(({ channel: { id } }) => id === channelData.channel.id)
    ) {
      setChannels([...channels, channelData]);
    }
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

  return (
    <>
      <AddChannel onChannelAdded={onChannelAdded} />

      {channels.map(({ channel: { name, id }, videos }) => (
        <ChannelContainer key={id}>
          <h3>{name}</h3>
          <VideosContainer>
            {videos.map((video) => (
              <VideoItem>
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
